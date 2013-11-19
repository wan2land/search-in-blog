# -*- coding:utf-8 -*-

def parser( formula ) :
	operators = list('+-*/=')

	output_operator = []
	output_number = []

	buff = []

	for c in formula :
		if c in operators :
			output_number.append( int(''.join(buff)) )
			buff = []
			output_operator.append(c)
		else :
			buff.append(c)
	
	if len(buff) > 0 :
		output_number.append( int(''.join(buff)) )
	
	return output_number, output_operator[0:len(output_number)-1]


if __name__ == "__main__" :
	print parser('6+355*23')