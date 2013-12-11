# -*- coding:utf-8 -*-
"""
웹에서 검색결과가 312+134*1234 이런식으로 들어옴.
이 식을 파싱하는 모듈.
"""

def parser( formula ) :
	operators = list('+-*/=')

	output_operator = []
	output_number = []

	buff = []

	for c in formula :
		if c in operators :
			if len(buff) > 0 :
				output_number.append( int(''.join(buff)) )
				buff = []
				output_operator.append(c)
		else :
			if c in list('0123456789') :
				buff.append(c)
	
	if len(buff) > 0 :
		output_number.append( int(''.join(buff)) )
	
	return output_number, output_operator[0:len(output_number)-1]


if __name__ == "__main__" :
	print parser('6+-355*+23+undefasdf')