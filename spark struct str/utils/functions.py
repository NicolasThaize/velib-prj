from pyspark.sql.functions import col, from_json

def parseKafkaData(df, schema): # Return a parsed json string kafka df
  return df.select(from_json(col('value'), schema).alias('jsonData')).select('jsonData.*')
