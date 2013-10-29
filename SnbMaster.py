import Config
import SnbSpatialLibrary as Snb

config = Config.fromJson( "mysql.json" )

rtree = Snb.RTree()
print rtree