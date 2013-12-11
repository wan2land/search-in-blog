# -*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors

"""
MySQLdb 모듈이 조금 복잡하게 사용되는 것 같아, 조금 더 간단한 인터페이스로 제작한 래퍼 모듈(Wrapper Module).
tableExists는 해당 테이블이 현재 db에 존재하는지 확인하고, getAutoIncrement는 현제 테이블에서 앞으로 사용될
autoincrement값을 가져온다.
"""

#for Caching!
connect_pool = {}

class PySql :
	def __init__(self, host = "127.0.0.1", port = 3306, dbname = "test", timeout = 5, **kwargs) :
		self.name = dbname
		self.conn = MySQLdb.connect(host = host, port = int(port),
				user = kwargs['user'], passwd = kwargs['password'],
				db = dbname, connect_timeout=timeout )
		print "Connect!"
	
	def query( self, query, args = None ) :
		c = self.conn.cursor()
		c.execute(query, args)

		self.conn.commit();

		return c

	def getName(self) :
		return self.name

	def getConnector(self) : 
		return self.conn

	def tableExists( self, tname ) :
		c = self.query("""SELECT COUNT(*) FROM `information_schema`.`tables`
			WHERE `TABLE_NAME` = %s AND `TABLE_SCHEMA` = %s""", (tname, self.name))

		return bool( c.fetchone()[0] )

	def getAutoIncrement( self, tname ) :
		c = self.query("""SELECT `AUTO_INCREMENT` FROM `information_schema`.`tables`
			WHERE `TABLE_NAME` = %s AND `TABLE_SCHEMA` = %s""", (tname, self.name))

		return c.fetchone()[0]


def connect( host, port = 3306, dbname = "test", **kwargs ) :
	connect_key = host + ":" + str(port) + "#" + dbname
	if connect_key in connect_pool : 
		return connect_pool[connect_key]

	try :
		print "Connecting.." + connect_key
		connect_pool[connect_key] = PySql( host, port, dbname = dbname, **kwargs )
	except :
		print "Timeout!"
		return None

	return connect_pool[connect_key]