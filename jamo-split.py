# -*- coding:utf-8 -*-
import MySQLdb
import re
from Jamo import divText

conn = MySQLdb.connect(host="localhost",user="root",passwd="rooroo123",db="siblo")
dir(conn)

x = conn.cursor()
x.execute("SET NAMES utf8")

#x.execute("""SELECT `idx`, `dong` FROM `sib_dong_t`""")
x.execute("""SELECT `id`, `name` FROM `siblo_locations`""")
rows = x.fetchall()
for row in rows :
	idx = row[0]
	gu = row[1]
	name = ''.join( divText( gu.decode("utf-8") ) )
	#x.execute("""UPDATE `sib_dong_t` SET `name` = %s WHERE `idx` = %s """, (name.encode('utf-8'), idx))
	x.execute("""UPDATE `siblo_locations` SET `keyword` = %s WHERE `id` = %s """, (name.encode('utf-8'), idx))

conn.commit()
conn.close()


#insert into siblo_locations(name, address, geo) select dong as name, concat(si, " ", gu, " ", dong) as address, polygon as geo from sib_dong_t;
#insert into siblo_locations(name, address, geo) select gu as name, concat(si, " ", gu) as address, polygon as geo from sib_gu_t;
#delete from siblo_locations where geo is null;

