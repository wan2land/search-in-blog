# -*- coding:utf-8 -*-
import json

"""
그냥 config파일 가져와서 파싱하는 모듈.
"""

def fromJson( path ) :
	fp = open( 'config/' + path )
	data = json.load( fp )
	return data

