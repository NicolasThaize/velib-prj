from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, ArrayType, StringType, TimestampType

MONGO_DB_CONNECTION_STRING = "mongodb://root:myPwd@localhost:27017/?authMechanism=DEFAULT"
MONGO_DB_NAME = "velibprj"

station_cluster_scheme = StructType([ \
  StructField('id_station', StringType(), False), \
  StructField('cluster_label', IntegerType(), False)
])

velib_fields_scheme = StructType([ \
  StructField('name', StringType(), False), \
  StructField('stationcode', StringType(), False), \
  StructField('ebike', IntegerType(), False), \
  StructField('mechanical', IntegerType(), False), \
  StructField('coordonnees_geo', ArrayType(FloatType()), False), \
  StructField('numbikesavailable', IntegerType(), False), \
  StructField('numdocksavailable', IntegerType(), False), \
  StructField('capacity', IntegerType(), False), \
  StructField('is_renting', StringType(), False), \
  StructField('is_installed', StringType(), False), \
  StructField('nom_arrondissement_communes', StringType(), False), \
  StructField('is_returning', StringType(), False), \
  StructField('timestamp', TimestampType(), False)  
])
