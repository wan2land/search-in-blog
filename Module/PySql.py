import MySQLdb
import MySQLdb.cursors

#for Caching!
connect_pool = {}

class PySql :
	def __init__(self, host = "127.0.0.1", port = 3306, dbname = "test", timeout = 5, **kwargs) :
		self.name = dbname
		self.conn = MySQLdb.connect(host = host, port = int(port),
				user = kwargs['user'], passwd = kwargs['password'],
				db = dbname,  cursorclass=MySQLdb.cursors.DictCursor, connect_timeout=timeout )
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
		c = self.conn.cursor()
		c.execute("""SET NAMES utf8""")
		c.execute("""SELECT COUNT(*) AS count FROM `information_schema`.`tables`
			WHERE `TABLE_NAME` = %s and `TABLE_SCHEMA` = %s""", (tname, self.name))

		return bool( c.fetchone()['count'] )



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