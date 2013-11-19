# -*- coding:utf-8 -*-
import warnings

import Geo.Converter as Converter
import Module.PySql as PySql

from Module.LimTokenizer import LimTokenizer, ords
from multiprocessing import Process, Queue
from random import randint




warnings.filterwarnings('error')



class MyMaster :
	def __init__(self, name, connector) :

		self.name = name
		self.connector = connector
		self.cache_item = dict()

		self.init()

	def init(self) :
		# Original Table Create!!
		if not self.connector.tableExists( self.name ) :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`g` geometry NOT NULL,
				`text` text,
				PRIMARY KEY (`idx`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % ( self.name, ))

		if not self.connector.tableExists( self.name + "_meta" ) :
			self.connector.query("""CREATE TABLE `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`name` varchar(20) DEFAULT NULL,
				`value` text DEFAULT NULL,
				`document_idx` int(11) DEFAULT NULL,
				PRIMARY KEY (`idx`),
				KEY `document_idx` (`document_idx`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % ( self.name + "_meta", ))

		self.idx = self.connector.getAutoIncrement( self.name )

	def insert(self, values) :

		g = values[0]
		text = values[1]

		idx = self.idx

		self.connector.query("""INSERT INTO `{}`(`idx`, `g`, `text`) VALUES (%s, GeomFromText(%s), %s);"""
				.format(self.name),
				(idx, Converter.geo2text(g), text) )
		
		if len(values) > 2 :
			for k,v in values[2].iteritems() :
				self.connector.query("""INSERT INTO `{}`(`name`, `value`, `document_idx`) VALUES (%s, %s, %s);"""
						.format(self.name + "_meta"),
						(k, v, idx) )
		

		self.idx = self.idx + 1

		return idx

	def getbyIdx(self, idx) :
		if idx not in self.cache_item :
			c = self.connector.query("""SELECT AsText(`g`), `text` FROM `%s` WHERE `idx` = %s""" % (self.name, idx ) )
			self.cache_item[idx] = c.fetchone()

			c = self.connector.query("""SELECT `name`, `value` FROM `%s` WHERE `document_idx` = %s"""
					% (self.name + "_meta", idx)
				)
			options = dict()
			for item in c.fetchall() :
				options[item[0]] = item[1]

			if len(options.keys()) > 0 :
				self.cache_item[idx] = self.cache_item[idx] + (options, )

		return self.cache_item[idx]

	def destroy(self) :
		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name ,))
		except :
			pass

		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_meta" ,))
		except :
			pass			

		print "Remove All Master Table!"





class MySpatial :
	def __init__( self, name, connector ) :

		self.name = name
		self.connector = connector

		self.init()

	def init(self) :

		if not self.connector.tableExists( self.name + "_spatial" ) :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
					`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
					`g` geometry NOT NULL,
					`document_idx` int(11),
					PRIMARY KEY (`idx`),
					SPATIAL KEY (`g`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (self.name + "_spatial")
			)

	def insert(self, g, idx) :
		self.connector.query("""INSERT INTO `%s`(`g`, `document_idx`) VALUES(GeomFromText('%s'), '%s');"""
				% (self.name + "_spatial", Converter.geo2text(g), idx) )

		return True

	def search(self, operator, shapely) :

		ret = Converter.geo2text( shapely )
		
		stmt = self.connector.query("""SELECT `document_idx` FROM `%s` WHERE %s(GeomFromText('%s'), `g`)"""
				% (self.name + "_spatial", operator, ret) )
		
		result = [ int(x[0]) for x in stmt.fetchall() ]

		return result

	def destroy(self) :
		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_spatial" ,))
		except :
			pass

		print "Remove All Spatial Table!"




class MyNoneFulltext :
	def __init__( self, name, connector, tokenizer = None ) :
		self.name = name
		self.connector = connector
		
		self.init()

	def init(self) :
		if not self.connector.tableExists(self.name + '_nidxp') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`text` text NOT NULL,
				`document_idx` int(11) NOT NULL,
				PRIMARY KEY (`idx`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (self.name + '_nidxp')
			)

	def insert(self, text, idx ) :

		try :
			self.connector.query("""INSERT IGNORE INTO `{}`
					SET `text` = %s, `document_idx` = %s """
					.format( self.name + '_nidxp'),
					( text, idx ) )
		except :
			print "Error, this is not strings!", idx
		

		return True


	def searchByWord(self, word) :
		stmt = self.connector.query("""SELECT SQL_NO_CACHE `document_idx` FROM `{}` WHERE `text` LIKE %s"""
				.format(self.name + '_nidxp'),
				('%'+word+'%', ) )
		return [ int(x[0]) for x in stmt.fetchall() ]
	
	def search(self, text) :
		result = []
		for word in text.split() :
			if len( result ) == 0 :
				result =  self.searchByWord(word)
			else :
				result = list(set(result) & set( self.searchByWord(word) ))

		return result

	
	def destroy(self) :
		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_idx",))
		except :
			pass

		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_idxp" ,))
		except :
			pass

		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_nidxp" ,))
		except :
			pass


		print "Remove All None Fulltext Table!"







class MyFulltext :
	def __init__( self, name, connector, tokenizer = None ) :
		self.name = name
		self.connector = connector
		
		if tokenizer is None :
			self.tokenizer = LimTokenizer
		else :
			self.tokenizer = tokenizer

		self.init()

	def init(self) :
		if not self.connector.tableExists(self.name + '_idx') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word` varchar(50) NOT NULL DEFAULT '',
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word`),
				KEY (`word`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (self.name + "_idx", )
			)

		if not self.connector.tableExists(self.name + '_idxp') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word_idx` int(11) NOT NULL,
				`document_idx` int(11) NOT NULL,
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word_idx`,`document_idx`),
				KEY (`word_idx`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (self.name + '_idxp')
			)

	def insert(self, text, idx ) :
		for word in self.tokenizer.doit(text) :
			try :
				self.connector.query("""INSERT IGNORE INTO `%s`
						SET `word` = '%s'""" % ( self.name + '_idx', word ))
				self.connector.query("""INSERT IGNORE INTO `%s`
						SET `word_idx` = (SELECT `idx` FROM `%s` WHERE `word` = '%s' limit 1),
						`document_idx` = '%s' """ % ( self.name + '_idxp',
						self.name + '_idx' , word, idx))
			except :
				print "Error, this is not strings!", idx, ":", word
				print ords(word)
				continue
			

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

	def destroy(self) :
		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_idx",))
		except :
			pass

		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_idxp" ,))
		except :
			pass

		try :
			self.connector.query("""DROP TABLE `%s`""" % (self.name + "_nidxp" ,))
		except :
			pass

		print "Remove All Fulltext Table!"









class Searcher :

	def __init__(self, name, servers, prefix = "_siblo_", fulltext = True ) :

		self.prefix = prefix
		self.name = name

		# Main Connector!!
		self.master = MyMaster( prefix + name, connector = self._makeConnection( **servers[0] ) )

		self.servers = []

		for server in servers :
			connector = self._makeConnection( **server )
			if connector is None :
				continue

			if fulltext :
				full = MyFulltext( prefix + name, connector = connector )
			else :
				full = MyNoneFulltext( prefix + name, connector = connector )

			spatial = MySpatial( prefix + name, connector = connector )

			self.servers.append({"fulltext" : full, "spatial" : spatial})

	def init(self) :
		self.master.init()

		for server in self.servers :
			server['fulltext'].init()
			server['spatial'].init()			

	def _makeConnection( self, host = "127.0.0.1", user = "root", password = "root", dbname = "test" ) :
		return PySql.connect(host = host, user = user, password = password, dbname = dbname)



	def insert( self, *values ) :


		def insertDatabase( server, values ) :
			# Source Start

			fulltext = server['fulltext']
			spatial = server['spatial']

			for value in values :

				idx = value[0]

				spatial.insert( value[1], idx )
				fulltext.insert( value[2], idx )

		jobs = []
		revalues = []

		for value in values :
			revalues.append( (self.master.insert( value ), ) + value  )

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



	def destroy( self ) :
		def destroyDatabase( server ) :
			# Source Start

			fulltext = server['fulltext']
			spatial = server['spatial']

			fulltext.destroy()
			spatial.destroy()

		jobs = []

		self.master.destroy()

		for server in self.servers :
			jobs.append(
					Process( target = destroyDatabase, args = ( server, ) )
			)

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True
