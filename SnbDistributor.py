# -*- coding:utf-8 -*-
import Config
from multiprocessing import Process, Queue

"""
RTree로 최상단 노드의 mbb추가해야함.
그리고 balence과정을 통해서 각 노드간에 통신이 이루어져야함.
"""
class Distributor :

	def __init__(self, name, servers) :
		self.servers = servers

	def multiQuery( self, query, values ) :

		def insertDatabase( idx, server, query, values, output ) :
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

		result = Queue()

		jobs = []
		idx = 0
		for server in self.servers :
			jobs.append( Process( target = insertDatabase, args = (idx, server, query, values[idx:][::len(self.servers)] ,result)) )
			idx = idx + 1

		for job in jobs : job.start()
		for job in jobs : job.join()

		return True

	def multiSearch( self, keyword ) :
		
		def selectDatabase( idx, server, keyword, output ) :
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

			cursor.execute("""SELECT * FROM `test`""")
			output.put( cursor.fetchall() )

			cursor.close()
			db.close()		

		result = Queue()

		jobs = []
		idx = 0
		for server in self.servers :
			jobs.append( Process( target = selectDatabase, args = (idx, server, keyword ,result)) )
			idx = idx + 1

		for job in jobs : job.start()

		ret = []
		for job in jobs : 
			ret = ret + list( result.get() )
			job.join()

		return ret



if __name__ == '__main__':

	config = Config.fromJson( "parallel.json" )

	dist = Distributor("hello", config)

	dist.multiQuery("""INSERT INTO `test`(`num`) VALUES (%s)""", [(value,) for value in [10,20,23,25,17,70,34,226]])
	
	#print dist.multiSearch( "keyword" )
#	print multiSearch(config, )

