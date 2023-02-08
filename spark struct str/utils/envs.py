from pyspark.sql.types import StructType,StructField,IntegerType, FloatType, ArrayType, StringType, DateType

velib_scheme = StructType([ \
  StructField("datasetid", StringType(), False), \
  StructField("recordid", StringType(), False), \
  StructField("fields", StructType([ \
    StructField('name', StringType(), False), \
    StructField('stationcode', IntegerType(), False), \
    StructField('ebike', IntegerType(), False), \
    StructField('mechanical', IntegerType(), False), \
    StructField('coordonnees_geo', ArrayType(FloatType()), False), \
    StructField('numbikesavailable', IntegerType(), False), \
    StructField('numdocksavailable', IntegerType(), False), \
    StructField('capacity', IntegerType(), False), \
    StructField('is_renting', StringType(), False), \
    StructField('is_installed', StringType(), False), \
    StructField('nom_arrondissement_communes', StringType(), False), \
    StructField('is_returning', StringType(), False) \
  ]), False), \
  StructField("geometry", StructType([ \
    StructField('type', StringType(), False), \
    StructField('coordinates', ArrayType(FloatType()), False) \
  ]), False), \
  StructField("record_timestamp", StringType(), False), \
])