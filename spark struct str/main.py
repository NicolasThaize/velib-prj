from pyspark.sql import SparkSession
from utils.envs import velib_fields_scheme
from utils.functions import parseKafkaData, maxElecVelibs, maxMechaVelibs, nbSlotsVelibs, basicAverage

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

df = df.selectExpr("CAST(value AS STRING)") # Casting binary values to string
df = parseKafkaData(df, velib_fields_scheme) # Parse string values to a structured df 

queryBaiscAvg = basicAverage(df)

queryBaiscAvg.writeStream.format('console').outputMode('update').start()

spark.streams.awaitAnyTermination()