# -*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import inspect

import Geo.Converter as Converter
import Module.PySql as PySql
import Module.FullText as FullText


class Searcher :

	def __init__(self, name, **kwargs) :
		self.name = name
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
				"within" : "MBRWithin",
			}

		ret = Converter.geo2text( shapely )
		
		if (ret is False) :
			return False

		stmt = self.connector.query("""SELECT `data` FROM `%s`
			WHERE %s(GeomFromText('%s'), `g`)""" % (self.name + "_spatial", type_map[type.lower()],ret) )
		
		result = stmt.fetchall()

		if ( keyword is not None ) :
			ret = self.fulltext.searchByText( keyword )
			print ret


		return result





