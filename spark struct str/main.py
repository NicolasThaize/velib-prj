from pyspark.sql import SparkSession
from utils.envs import velib_fields_scheme
from utils.functions import parseKafkaData, maxElecVelibs, maxMechaVelibs, nbSlotsVelibs

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

maxMechVelibs = maxMechaVelibs(df)

maxMechVelibs.writeStream.format('console').outputMode('append').start()

spark.streams.awaitAnyTermination()