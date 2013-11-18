# -*- coding:utf-8 -*-
import Geo.Converter as Converter
import Module.PySql as PySql

from Module.FullText import StandardTokenizer
from multiprocessing import Process, Queue
from random import randint

class MyMaster :
	def __init__(self, name, connector) :

		self.name = name
		self.connector = connector
		self.cache_item = dict()

		# Original Table Create!!
		if not connector.tableExists( name ) :
			connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`g` geometry NOT NULL,
				`text` text,
				PRIMARY KEY (`idx`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % ( name, ))

		self.idx = connector.getAutoIncrement( name )

	def insert(self, g, text) :
		idx = self.idx

		self.connector.query("""INSERT INTO `%s`(`idx`, `g`, `text`) VALUES ('%s', GeomFromText('%s'), '%s');"""
				% (self.name, idx, Converter.geo2text(g), text) )

		self.idx = self.idx + 1

		return idx

	def getbyIdx(self, idx) :
		if idx not in self.cache_item :
			c = self.connector.query("""SELECT AsText(`g`), `text` FROM `%s` WHERE `idx` = %s""" % (self.name, idx ) )
			self.cache_item[idx] = c.fetchone()

		return self.cache_item[idx]


class MySpatial :
	def __init__( self, name, connector ) :

		self.name = name
		self.connector = connector

		if not connector.tableExists( name + "_spatial" ) :
			connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
					`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
					`g` geometry NOT NULL,
					`data` int(11),
					PRIMARY KEY (`idx`),
					SPATIAL KEY (`g`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (name + "_spatial")
			)

	def insert(self, g, idx) :
		self.connector.query("""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');"""
				% (self.name + "_spatial", Converter.geo2text(g), idx) )

		return True

	def search(self, operator, shapely) :


		ret = Converter.geo2text( shapely )
		
		stmt = self.connector.query("""SELECT `data` FROM `%s` WHERE %s(GeomFromText('%s'), `g`)"""
				% (self.name + "_spatial", operator, ret) )
		
		result = [ int(x[0]) for x in stmt.fetchall() ]

		return result



class MyFulltext :
	def __init__( self, name, connector, tokenizer = None ) :
		self.name = name
		self.connector = connector
		
		if tokenizer is None :
			self.tokenizer = StandardTokenizer
		else :
			self.tokenizer = tokenizer

		if not connector.tableExists(name + '_idx') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word` varchar(50) NOT NULL DEFAULT '',
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word`),
				KEY (`word`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (name + "_idx", )
			)

		if not connector.tableExists(name + '_idxp') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word_idx` int(11) NOT NULL,
				`document_idx` int(11) NOT NULL,
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word_idx`,`document_idx`),
				KEY (`word_idx`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (name + '_idxp')
			)

	def insert(self, text, idx ) :
		for word in self.tokenizer.doit(text) :
			self.connector.query("""INSERT IGNORE INTO `%s`
					SET `word` = '%s'""" % ( self.name + '_idx', word ))
			self.connector.query("""INSERT IGNORE INTO `%s`
					SET `word_idx` = (SELECT `idx` FROM `%s` WHERE `word` = '%s' limit 1),
					`document_idx` = '%s' """ % ( self.name + '_idxp',
					self.name + '_idx' , word, idx))

		return True

	def searchByWord(self, word) :
		stmt = self.connector.query("""SELECT `document_idx` FROM `%s` WHERE `word_idx` in (SELECT `idx` FROM `%s` WHERE `word` = '%s')"""
				% ( self.name + '_idxp', self.name + '_idx', word))
		return [ int(x[0]) for x in stmt.fetchall() ]
	
	def search(self, text) :
		result = []
		for word in self.tokenizer.doit(text) :
			if len( result ) == 0 :
				result =  self.searchByWord(word)
			else :
				result = list(set(result) & set( self.searchByWord(word) ))

		return result


class Searcher :

	def __init__(self, name, servers, prefix = "_siblo_") :

		self.prefix = prefix
		self.name = name

		# Main Connector!!
		self.master = MyMaster( prefix + name, connector = self._makeConnection( **servers[0] ) )

		self.servers = []

		for server in servers :
			connector = self._makeConnection( **server )
			if connector is None :
				continue

			fulltext = MyFulltext( prefix + name, connector = connector )
			spatial = MySpatial( prefix + name, connector = connector )

			self.servers.append({"fulltext" : fulltext, "spatial" : spatial})

			

	def _makeConnection( self, host = "127.0.0.1", user = "root", password = "root", dbname = "test" ) :
		return PySql.connect(host = host, user = user, password = password, dbname = dbname)

	"""
	def insert( self, shapely, documents = None ) :


		def insertDatabase( idx, name, server, shapely, documents, output ) :
			# Source Start
			connector = server['connector']
			fulltext = server['fulltext']

			idx = 0
			if documents is not None :
				idx = fulltext.addDocument( documents )

			ret = Converter.geo2text( shapely )

			if ret is False : 
				return False

			connector.query(""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');"" % (name + "_spatial", ret, idx) )	

		
		result = Queue()

		jobs = []
		idx = randint(0,1)
		
		server = self.servers[idx]
		jobs.append( Process( target = insertDatabase, args = (idx, self.name, server, shapely, documents ,result)) )

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True
	"""

	def insertmany( self, *values ) :


		def insertDatabase( server, values ) :
			# Source Start

			fulltext = server['fulltext']
			spatial = server['spatial']

			for value in values :

				idx = value[2]

				fulltext.insert( value[1], idx )
				spatial.insert( value[0], idx )

		jobs = []
		revalues = []

		for value in values :
			revalues.append( value + (self.master.insert( value[0], value[1] ), ) )

		i = 0
		for server in self.servers :
			jobs.append(
					Process( target = insertDatabase, args = ( server, revalues[i:][::len(self.servers)]) )
			)
			i = i + 1

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True

	def search( self, operator, shapely, keyword = None, option = "index" ) :

		def selectDatabase( server, operator, shapely, keyword, output ) :
			# Source Start
			fulltext = server['fulltext']
			spatial = server['spatial']


			ret = spatial.search( operator, shapely )
			if keyword is not None :
				ret = list(set(ret) & set( fulltext.search( keyword ) ))
			
			output.put(ret)

		result = Queue()

		jobs = []

		for server in self.servers :
			jobs.append( Process( target = selectDatabase, args = ( server, operator, shapely, keyword ,result)) )

		for job in jobs : job.start()

		results = []
		for job in jobs : 
			results = results + list( result.get() )
			job.join()

		if option == "index" :
			return results

		return [self.master.getbyIdx( result ) for result in results]






