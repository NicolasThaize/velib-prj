from pyspark.sql import SparkSession
from utils.envs import velib_fields_scheme, station_cluster_scheme
from utils.functions import parseKafkaData, basicAverage, groupedAverage
from utils.classes import MongoForeachSinker

spark = SparkSession.builder.appName('velib-prj') \
  .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.mongodb.spark:mongo-spark-connector_2.12:10.1.1') \
  .getOrCreate() # Spark session w/ kafka and mongodb dependencies
spark.sparkContext.setLogLevel("ERROR") # Less logs

station_groups = spark.read.option('header', True).csv('./station_clusters.csv', schema=station_cluster_scheme)

raw_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "stations_raw_data") \
  .load() # Subscribing to kafka topic

string_casted_df = raw_df.selectExpr("CAST(value AS STRING)") # Casting binary values to string
structured_df = parseKafkaData(string_casted_df, velib_fields_scheme) # Parse string values to a structured df 
stations_with_groups = structured_df.join(station_groups, structured_df['stationcode'] == station_groups['id_station'], 'inner')

queryBasicAvg = basicAverage(structured_df)

queryGroupedAvg = groupedAverage(stations_with_groups)

queryBasicAvg.writeStream.outputMode('update').foreach(MongoForeachSinker(collection='stationsBasicAvg')).start()  
queryGroupedAvg.writeStream.outputMode('update').foreach(MongoForeachSinker(collection='stationsGroupedAvg')).start()

spark.streams.awaitAnyTermination()
