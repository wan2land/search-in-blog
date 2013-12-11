# -*- coding:utf-8 -*-
import inspect

import Geo.Converter as Converter
import Module.PySql as PySql


"""
Search'n Blog Project
Snb Connector, Mysql 활용하여.. 만듦.

공간문서검색에서 문서검색에 해당하는 부분.
각 문서당 테이블을 3개 생성하여서 사용함. 나머지 2개에는 인덱스와 토큰들을 저장하여서 효율을 끌어올림.
실제로 성능평가 해보면 (캐쉬를 사용하지 않는다면..) 적은 숫자에서는 성능이 낮지만, 갯수가 많아질 수록 일반 fulltext보다 결과가 빨라짐.
"""

class SnbException(Exception):	# 지원하는 Geometry 타입이 아닌 경우
	def __init__(self, str):
		self.str = str


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
	
	def __init__(self, host = "localhost", port = 3306, **args) :
		self.connector = PySql.connect(host = host, port = int(port), user = args['user'], passwd = args['password'], dbname = args['database'] )

		#인코딩 초기화..!! utf8지정해주었다면 :)
		if 'encoding' not in args.keys() :
			print "Encoding..."


	def selectTable(self, name, **args) :
		return SnbTable(name, connector = self.connector, **args)

class SnbOrigin :
	def __init__(self, name, connector) :
		self.name = name
		self.connector = connector
		if not connector.tableExists(name) :
			connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`text` text,
				PRIMARY KEY (`idx`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (name, ))
			
		self.pointer = connector.getAutoIncrement( name )

	def addDocument(self, text) :
		
		idx = self.pointer

		self.connector.query("""INSERT INTO `%s`
				SET `idx` = '%s', `text`= '%s';""" % ( self.name, str(idx), text) )

		self.pointer = self.pointer + 1
		return idx

	def removeDocument(self, idx) :

		self.connector.query("""DELETE FROM `%s` WHERE `idx` = '%s'""" % ( self.name , idx ))
		self.connector.query("""DELETE FROM `%s` WHERE `document_idx` = '%s'""" % ( self.name + '_idxp' , idx ))


	def searchByWord(self, word) :
		stmt = self.connector.query("""SELECT `document_idx` FROM `%s`
				WHERE `word_idx` IN ( SELECT `idx` FROM `%s` where `word` = '%s')"""
				% ( self.name + '_idxp', self.name + '_idx', word, ))

		return [ int(x[0]) for x in stmt.fetchall() ]
	
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




class SnbTable :

	def __init__(self, name, connector, tokenizer = None, origin = None) :
		self.name = name
		self.connector = connector

		if tokenizer is not None :
			self.tokenizer = tokenizer
		else :
			self.tokenizer = StandardTokenizer

		self.origin = origin
		if origin == "default" :
			self.origin = SnbOrigin( name, connector )

		if not self.connector.tableExists(name + '_idx') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word` varchar(50) NOT NULL DEFAULT '',
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word`),
				KEY (`word`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (name + "_idx", )
			)

		if not self.connector.tableExists(name + '_idxp') :
			self.connector.query("""CREATE TABLE IF NOT EXISTS `%s` (
				`idx` int(11) unsigned NOT NULL AUTO_INCREMENT,
				`word_idx` int(11) NOT NULL,
				`document_idx` int(11) NOT NULL,
				PRIMARY KEY (`idx`),
				UNIQUE KEY (`word_idx`,`document_idx`),
				KEY (`word_idx`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;""" % (name + '_idxp')
			)



	def addDocument(self, text, idx = None ) :
		
		if idx is None and self.origin is not None :
			idx = self.origin.addDocument( text )
		elif idx is None and self.origin is None :
			raise SnbException("idx, origin 둘다 설정되어 있지 않습니다.")

		for word in self.tokenizer.doit(text) :
			self.connector.query("""INSERT IGNORE INTO `%s`
					SET `word` = '%s'""" % ( self.name + '_idx', word ))
			self.connector.query("""INSERT IGNORE INTO `%s`
					SET `word_idx` = (SELECT `idx` FROM `%s` WHERE `word` = '%s' limit 1),
					`document_idx` = '%s' """ % ( self.name + '_idxp',
					self.name + '_idx' , word, idx))

		return idx

	def removeDocument(self, idx) :

		self.connector.query("""DELETE FROM `%s` WHERE `idx` = '%s'""" % (self.name, idx) )
		self.connector.query("""DELETE FROM `%s` WHERE `document_idx` = '%s'""" % ( self.name + '_idxp', idx) )


	def searchByWord(self, word) :
		stmt = self.connector.query("""SELECT `document_idx` FROM `%s`
		WHERE `word_idx` in (select `idx` from `%s` where `word` = '%s')""" % ( self.name + '_idxp', self.name + '_idx', word))
		return [ int(x[0]) for x in stmt.fetchall() ]
	
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
	"""
	def _getAutoIncrement(self, name) :
		c = self.connector.cursor()
		c.execute(""show table status like '%s'" % name )
		return c.fetchone()['Auto_increment']
	"""
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




