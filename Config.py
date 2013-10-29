import json

def fromJson( path ) :
	fp = open( 'config/' + path )
	data = json.load( fp )
	return data

