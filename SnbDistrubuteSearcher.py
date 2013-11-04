# -*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import inspect

import Geo.Converter as Converter
import Module.PySql as PySql
import Module.FullText as FullText


class Searcher :

	def __init__(self, name, servers ) :
		self.servers = servers
		self.name = name

		def checkDatabase(server) :
			import MySQLdb

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
			db = MySQLdb.connect(host = host, user = user, passwd = password, db = db)
			cursor = db.cursor()

			cursor.executemany(query, values)

			db.commit()
			cursor.close()
			db.close()		


		jobs = []
		for server in self.servers :
			jobs.append( Process( target = checkDatabase, args = (server)) )

		for job in jobs : job.start()
		for job in jobs : job.join()


		self.connector = PySql.connect( **kwargs )
		self.fulltext = FullText.SnbTable( name, connector = self.connector.getConnector() )

		if ( not self.connector.tableExists( name + "_spatial" ) ) :
			self.connector.query("""CREATE TABLE `%s` (
					`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
					`g` geometry NOT NULL,
					`data` int(11),
					PRIMARY KEY (`idx`),
					SPATIAL KEY (`g`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8;""" % (name + "_spatial") )


	def insert( self, shapely, documents = None ) :

		idx = 0
		if ( documents is not None ) :
			idx = self.fulltext.addDocument( documents )

		ret = Converter.geo2text( shapely )
		
		if (ret is False) :
			return False

		#print shapely
		self.connector.query("""INSERT INTO `%s`(`g`, `data`) VALUES(GeomFromText('%s'), '%s');""" % (self.name + "_spatial", ret, idx) )

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





