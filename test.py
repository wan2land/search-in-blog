# -*- coding:utf-8 -*-
import SnbLibrary
import time
"""
conn = SnbLibrary.connect(host = "localhost", user="root", password="root", database="siblo")

my_table = conn.selectTable('testdocs')



print my_table.searchByText('임한가람이랑')


my_table.removeDocument(7)

print my_table.searchByText('임한가람이랑')
"""
def foo() :
	for i in range(0,100) :
		yield i

for i in foo() :
	print i

