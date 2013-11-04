import Converter
try:
	Converter.text2geo("KK")
except Converter.geoTypeError as e:
	print('Error - it is not geometry', e.str)

try:
	Converter.geo2text("PP")
except Converter.geoTypeError as e:
	print('Error - it is not geometry', e.str)

str = "POLYGON((0 0,1 1,3 3))"

try:
	Converter.convertPolygon(str)
except Converter.polyAreaError as e:
	print('Error - it is not geometry', e.str)
