import MySQLdb
import MySQLdb.cursors


class PySql :
	def __init__(self, host = "127.0.0.1", port = 3306, **kwargs) :
		self.conn = MySQLdb.connect(host = host, port = int(port),
				user = kwargs['user'], passwd = kwargs['password'],
				db = kwargs['dbname'],  cursorclass=MySQLdb.cursors.DictCursor )
	
	def query( self, query ) :
		c = self.conn.cursor()
		c.execute(query)
		return c

	def getConnector(self) : 
		return self.conn

	def tableExists( self, name ) :
		c = self.conn.cursor()
		c.execute("""SELECT COUNT(*) AS count FROM `information_schema`.`tables` WHERE `table_name` = %s""", (name, ))

		return bool( c.fetchone()['count'] )



def connect( **kwargs ) :
	return PySql( **kwargs )