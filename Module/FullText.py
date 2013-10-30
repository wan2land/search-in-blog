# -*- coding:utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import inspect

import Geo.Converter as Converter
import Module.PySql as PySql
#import time

"""
Search'n Blog Project
Snb Connector, Mysql 활용하여.. 만듦.
"""

# 그냥 띄어쓰기로 된 토크나이저. 특수문자만 대충 제거해서 사용할 수 있음.. -_-; ㅋㅋㅋ
class StandardTokenizer :
	@staticmethod
	def doit(text) :
		for word in text.split() :
		
			word = word.strip('"')
			word = word.strip("'")
			word = word.strip(".")
			word = word.strip(",")

			if word.isspace() :
				continue

			yield word

class SnbConnector :
	
	connector = None

	def __init__(self, host = "localhost", port = 3306, **args) :
		self.connector = MySQLdb.connect(host = host, port = int(port), user = args['user'], passwd = args['password'], db = args['database'],  cursorclass=MySQLdb.cursors.DictCursor )

		#인코딩 초기화..!! utf8지정해주었다면 :)
		if 'encoding' not in args.keys() :
			c = self.connector.cursor()
			c.execute('SET NAMES utf8')


	def selectTable(self, name, **args) :
		return SnbTable(name, connector = self.connector, **args)

class SnbTable :

	name = None

	connector = None
	tokenizer = StandardTokenizer

	def __init__(self, name, connector, **args) :
		self.name = name
		self.connector = connector

		if 'tokenizer' in args.keys() and inspect.isclass( args['tokenizer'] ) :
			self.tokenizer = args['tokenizer']

		try :
			c = self.connector.cursor()
			query = 'show tables like \'' + name + '\''
			c.execute(query)
			if ( c.fetchone() is None ) :
				query = (
					'CREATE TABLE IF NOT EXISTS `' + name + '` ('
					'`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,'
					'`text` text,'
					'PRIMARY KEY (`idx`)'
					') ENGINE=InnoDB;'
					'CREATE TABLE IF NOT EXISTS `' + name + '_idx` ('
					'`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,'
					'`word` varchar(50) NOT NULL DEFAULT \'\','
					'PRIMARY KEY (`idx`),'
					'UNIQUE KEY (`word`),'
					'KEY (`word`)'
					') ENGINE=InnoDB;'
					'CREATE TABLE IF NOT EXISTS `' + name + '_idxp` ('
					'`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,'
					'`word_idx` int(11) NOT NULL,'
					'`document_idx` int(11) NOT NULL,'
					'PRIMARY KEY (`idx`),'
					'UNIQUE KEY (`word_idx`,`document_idx`),'
					'KEY (`word_idx`)'
					') ENGINE=InnoDB;'
				)
				c.execute(query)


		except MySQLdb.Error, e :
			print "makeTable Error!"
			print e[1]

	def addDocument(self, text) :
		
		c = self.connector.cursor()
		idx = self._getAutoIncrement( self.name )
		
		c.execute("""INSERT INTO `{}`
				SET `text`= %s """.format( self.name ), (text,))
		
		for word in self.tokenizer.doit(text) :
			c.execute("""INSERT IGNORE INTO `{}`
					SET `word` = %s""".format( self.name + '_idx' ) , (word, ))
			c.execute("""INSERT IGNORE INTO `{}`
					SET `word_idx` = (SELECT `idx` FROM `{}` WHERE `word` = %s limit 1),
					`document_idx` = %s """.format( self.name + '_idxp',
					self.name + '_idx' ), (word, idx))

		self.connector.commit()
		return idx

	def removeDocument(self, idx) :

		c = self.connector.cursor()

		c.execute("""DELETE FROM `{}` WHERE `idx` = %s""".format( self.name ), (idx, ))
		c.execute("""DELETE FROM `{}` WHERE `document_idx` = %s""".format( self.name + '_idxp' ), (idx, ))

		self.connector.commit()

	def searchByWord(self, word) :
		c = self.connector.cursor()
		c.execute("""SELECT `document_idx` FROM `{}` where `word_idx` in (select `idx` from `{}` where `word` = %s)""".format( self.name + '_idxp', self.name + '_idx'), (word, ))
		return [ int(x['document_idx']) for x in c.fetchall() ]
	
	def searchByText(self, text) :
		result = []
		for word in self.tokenizer.doit(text) :
			if len( result ) == 0 :
				result =  self.searchByWord(word)
			else :
				result = list(set(result) & set( self.searchByWord(word) ))
			#for idx in self.searchByWord(word) :
			#	if idx not in result :
			#		result.append(idx)

		return result

	def _getAutoIncrement(self, name) :
		c = self.connector.cursor()
		c.execute("""show table status like '%s'""" % name )
		return c.fetchone()['Auto_increment']

	#13.10.27 서대현 추가함, 근데 DB가 서대현이랑 전창완이랑 맞지 않아서 돌릴 수 없음
	#13.10.30 창완 SnbLibrary.py로 이동.
	"""def searchBySpatial(self) :
		c = self.connector.cursor()
		result = []
		query = "SELECT `id`, `name`, AsText(`geo`) as `geo`, `mbr` from geom"
		#query = "SELECT `id`, `name`, AsText(`geo`) as `geo`, `mbr` from new_table"
		c.execute(query)
		for x in c :
			geom = str(x['geo'])
			p = Converter.text2geo(geom)
			if p > 0 :
				result.append(p)
			#print x['id'], x['name'], x['geo'], x['mbr']
		return result
	"""

def connect(**args) :
	return SnbConnector(**args)




if __name__ == "__main__" :
	import time

	conn = connect(host = "localhost", user="root", password="root", database="siblo", port ="3306")

	my_table = conn.selectTable('testdocs')
	my_table.addDocument("동해물과 백두산이 마르고 닳도록")
	my_table.addDocument("남삼위에 저 소나무 철갑을 두른듯")
	my_table.addDocument("가을하늘 공활한데 높고 구름 없이")
	my_table.addDocument("이 기상과 이 맘으로 충성을 다하여")


	print my_table.searchByText("동해물과")




