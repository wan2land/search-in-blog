from random import randint


class RandomText :
	def __init__(self, text = None) :
		if text is None :
			text = open('test.txt').read()

		self.text_items = text.split(' ')
		self.text_items_size = len( self.text_items )

	def generate(self, size = 20) :
		ret = []
		for i in range(0, size) :
			ret.append( self.text_items[randint(0,self.text_items_size-1)] )

		return ' '.join(ret)