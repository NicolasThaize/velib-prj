from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType,StructField,IntegerType, FloatType, ArrayType, StringType, DateType

df_struct = StructType([ \
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
    StructField('is_returning', StringType(), False), \
  ]), False), \
  StructField("geometry", StructType([ \
    StructField('type', StringType(), False), \
    StructField('coordinates', ArrayType(FloatType()), False), \
  ]), False), \
  StructField("record_timestamp", StringType(), False), \
  ])

def parseKafkaData(df, schema): # Return a parsed json string kafka df
  return df.select(from_json(col('value'), schema).alias('jsonData')).select('jsonData.*')

spark = SparkSession.builder.appName('velib-prj') \
  .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1') \
  .getOrCreate() # Spark session w/ kafka dependencies
spark.sparkContext.setLogLevel("WARN") # Less logs

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "test1") \
  .load() # Subscribing to kafka topic

query = df.selectExpr("CAST(value AS STRING)") # Casting binary values to string
query = parseKafkaData(query, df_struct) # Parse string values to a structured df 

query.writeStream.format('console').outputMode('append').start().awaitTermination()
