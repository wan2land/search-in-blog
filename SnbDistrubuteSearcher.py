# -*- coding:utf-8 -*-
import Geo.Converter as Converter
import Module.PySql as PySql
import Module.FullText as FullText

from multiprocessing import Process, Queue
from random import randint

class Searcher :

	def __init__(self, name, servers, local ) :
		self.name = name

		self.connector = PySql.connect( **local )
		self.origin = FullText.SnbOrigin( name, connector = self.connector.getConnector() )

		self.servers = []

		for server in servers :
			if ":" in server['host'] :
				host = server['host'].split(':')[0]
			else :
				host = server['host']

			if "user" not in server :
				user = 'root'
			else :
				user = server['user']

			if "password" not in server :
				password = '1234'
			else :
				password = server['password']

			if "db" not in server :
				db = 'mydb'
			else :
				db = server['db']

			# Source Start
			connector = PySql.connect(host = host, user = user, password = password, dbname = db)
			fulltext = FullText.SnbTable( name, connector = connector.getConnector(), origin = None )
			
			self.servers.append( { "server" : server, "connector" : connector, "fulltext" : fulltext } )

			if ( not connector.tableExists( name + "_spatial" ) ) :
				connector.query("""CREATE TABLE `%s` (
						`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
						`g` geometry NOT NULL,
						`data` int(11),
						PRIMARY KEY (`idx`),
						SPATIAL KEY (`g`)
					) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (name + "_spatial") )


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

			connector.query("""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');""" % (name + "_spatial", ret, idx) )	

		
		result = Queue()

		jobs = []
		idx = randint(0,1)
		
		server = self.servers[idx]
		jobs.append( Process( target = insertDatabase, args = (idx, self.name, server, shapely, documents ,result)) )

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True


	def insertmany( self, *values ) :


		def insertDatabase( name, server, values, output ) :
			# Source Start
			connector = server['connector']
			fulltext = server['fulltext']

			for value in values :

				shapely = value[0]
				documents = value[1]
				idx = value[2]

				fulltext.addDocument( documents, idx )

				ret = Converter.geo2text( shapely )

				if ret is False : 
					return False

				connector.query("""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');""" % (name + "_spatial", ret, idx) )	

		result = Queue()

		jobs = []
		revalues = []

		for value in values :
			revalues.append( value + (self.origin.addDocument( value[1] ),) )

		idx = 0
		for server in self.servers :
			jobs.append( Process( target = insertDatabase, args = (self.name, server, revalues[idx:][::len(self.servers)], result)) )
			idx = idx + 1

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True

	def search( self, type, shapely, keyword = None ) :

		def selectDatabase( name, server, shapely, keyword, output ) :
			# Source Start
			connector = server['connector']
			fulltext = server['fulltext']

			type_map = {
					"contains" : "MBRContains",
					"disjoint" : "MBRDisjoint",
					"equal" : "MBREqual",
					"intersects" : "MBRIntersects",
					"overlaps" : "MBROverlaps",
					"touches" : "MBRTouches",
					"within" : "MBRWithin"
				}

			ret = Converter.geo2text( shapely )
			
			if (ret is False) :
				return False

			stmt = connector.query("""SELECT `data` FROM `%s`
				WHERE %s(GeomFromText('%s'), `g`)""" % (name + "_spatial", type_map[type.lower()],ret) )
			
			result = [ int(x['data']) for x in stmt.fetchall() ]
			#	if idx not in result :
			#		result.append(idx)

			#print result

			if ( keyword is not None ) :
				result = list(set(result) & set( fulltext.searchByText( keyword ) ))

			output.put( result )


		result = Queue()

		jobs = []

		for server in self.servers :
			jobs.append( Process( target = selectDatabase, args = (self.name, server, shapely, keyword ,result)) )

		for job in jobs : job.start()

		ret = []
		for job in jobs : 
			ret = ret + list( result.get() )
			job.join()

		return ret






