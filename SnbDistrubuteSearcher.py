# -*- coding:utf-8 -*-
import Geo.Converter as Converter
import Module.PySql as PySql
import Module.FullText as FullText

from multiprocessing import Process, Queue

class Searcher :

	def __init__(self, name, servers ) :
		self.servers = servers
		self.name = name

		def checkDatabase(name, server) :
			import Module.PySql as PySql
			import Module.FullText as FullText

			#arguments initer
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
			fulltext = FullText.SnbTable( name, connector = connector.getConnector() )
			if ( not connector.tableExists( name + "_spatial" ) ) :
				connector.query("""CREATE TABLE `%s` (
						`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
						`g` geometry NOT NULL,
						`data` int(11),
						PRIMARY KEY (`idx`),
						SPATIAL KEY (`g`)
					) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (name + "_spatial") )

		jobs = []
		for server in self.servers :
			jobs.append( Process( target = checkDatabase, args = (name, server)) )

		for job in jobs : job.start()
		for job in jobs : job.join()




	def insert( self, shapely, documents = None ) :


		def insertDatabase( idx, name, server, shapely, documents, output ) :
			import Geo.Converter as Converter
			import Module.PySql as PySql
			import Module.FullText as FullText

			#arguments initer
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
			fulltext = FullText.SnbTable( name, connector = connector.getConnector() )

			idx = 0
			if documents is not None :
				idx = fulltext.addDocument( documents )

			ret = Converter.geo2text( shapely )

			if ret is False : 
				return False

			connector.query("""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');""" % (name + "_spatial", ret, idx) )	

		result = Queue()

		jobs = []
		idx = 0
		for server in self.servers :
			jobs.append( Process( target = insertDatabase, args = (idx, self.name, server, shapely, documents ,result)) )
			idx = idx + 1

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True

	def search( self, type, shapely, keyword = None ) :
		
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

		stmt = self.connector.query("""SELECT `data` FROM `%s`
			WHERE %s(GeomFromText('%s'), `g`)""" % (self.name + "_spatial", type_map[type.lower()],ret) )
		
		result = [ int(x['data']) for x in stmt.fetchall() ]
		#	if idx not in result :
		#		result.append(idx)

		#print result

		if ( keyword is not None ) :
			result = list(set(result) & set( self.fulltext.searchByText( keyword ) ))


		return result





