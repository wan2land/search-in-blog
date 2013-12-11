# -*- coding:utf-8 -*-
from random import randint
"""
Random 텍스트 생성기
static/dummy.txt파일을 읽어들여서 단어별로 분류한 후,
generate() 호출 시, 20개(기본값)로 구성된 문장을 랜덤으로 생성해낸다.
"""
class RandomText :
	def __init__(self, text = None) :
		if text is None :
			text = open('static/dummy.txt').read()

		self.text_items = text.split(' ')
		self.text_items_size = len( self.text_items )

	def generate(self, size = 20) :
		ret = []
		for i in range(0, size) :
			ret.append( self.text_items[randint(0,self.text_items_size-1)] )

		return ' '.join(ret)