# -*- coding:utf-8 -*-
import Module.PySql as PySql
import re
from Jamo import divText

conn = PySql.connect(host="localhost",user="root",password="rooroo123",dbname="siblo")



geo = "POLYGON((37.55138234931889 127.0523357391357,37.54917078321267 127.0604038238525,37.54937493052542 127.0633220672607,37.55117820750436 127.0655107498169,37.55628158512069 127.0698022842407,37.55968364270852 127.0727634429932,37.55342373671084 127.0885562896729,37.55005541752973 127.0907878875732,37.54515577243407 127.085165977478,37.54018774792102 127.0829772949219,37.53685286085466 127.083535194397,37.53991551783298 127.0704460144043,37.54638071390078 127.0503187179565,37.55138234931889 127.0523357391357))"


name = "성동"
address = "건대입구"


keyword = ''.join( divText( name.decode('utf-8') ) ) #.encode('utf-8')
print isinstance( keyword, unicode )
print isinstance( keyword, str )

#conn.query("""INSERT `{}`(`name`, `address`, `keyword`, `geo`) VALUES ( %s,%s,%s,GeomFromText(%s) )"""
#		.format('siblo_locations'),
#		(name, address, keyword, geo) )


result = conn.query("""SELECT `id`, `name`, `address` FROM `siblo_locations`""" # WHERE `keyword` LIKE %s LIMIT 0, 20""",
#		(keyword, )
	)

kk = result.fetchall()[0][1]
print kk
print isinstance( kk, unicode )
print isinstance( kk, str )

exit()




#insert into siblo_locations(name, address, geo) select dong as name, concat(si, " ", gu, " ", dong) as address, polygon as geo from sib_dong_t;
#insert into siblo_locations(name, address, geo) select gu as name, concat(si, " ", gu) as address, polygon as geo from sib_gu_t;
#delete from siblo_locations where geo is null;

