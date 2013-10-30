import Config
import SnbSpatialLibrary as Snb

config = Config.fromJson( "parallel.json" )

for host in config :
	print host['secret']

#print config[1]


rtree = Snb.RTree()
print rtree