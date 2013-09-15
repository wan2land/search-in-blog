# -*- coding:utf-8 -*-
import SnbLibrary
import time

conn = SnbLibrary.connect(host = "localhost", user="root", password="root", database="siblo")

my_table = conn.selectTable('testdocs')

#my_table.addDocument("""동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세. 무궁화 삼천리 화려강산""")
#my_table.addDocument("""남산위에 저 소나무 철갑을 두른 듯 바람서리 불변함은 우리 기상일세. 무궁화 삼천리 화려강산""")
#my_table.addDocument("""동구 밖 과수원 길 아카시아 꽃이 활짝 폈네 소나무""")

start  = int(round(time.time() * 1000))

print my_table.searchByText('소나무 동구스 밥버거')

my_table.removeDocument(5)

print my_table.searchByText('소나무 동구스 밥버거')


print 'running time : ' + str( float( int(round(time.time() * 1000)) - start ) / 1000 )

#conn.getMySQLConnector()
