from pyspark.sql.functions import col, from_json, avg, window

def basicAverage(df): # Every 10 minutes, produce a day windowed df with average elec and mechanical bikes and anverage number of docks available by station 
  return df \
  .groupby(window(col('timestamp'), "1 hour", "10 minutes"), col('stationcode')) \
  .agg(avg('mechanical').alias('avg_mechanical'), avg('ebike').alias('avg_ebike'),  avg('numdocksavailable').alias('avg_numdocksavailable'))

def groupedAverage(df): # Every 10 minutes, produce a day windowed df with average elec and mechanical bikes and anverage number of docks available by station groups 
  return df.groupby(window(col('timestamp'), "1 days", "10 minutes"), col('cluster_label')) \
  .agg(avg('mechanical').alias('avg_mechanical'), avg('ebike').alias('avg_ebike'),  avg('numdocksavailable').alias('avg_numdocksavailable'))

def maxMechaVelibs(df): # Grouped by station code, number of mechanical velibs available
  return df.select(['stationcode', 'name', 'mechanical'])

def maxElecVelibs(df): # Grouped by station code, number of electrical velibs available
  return df.select(['stationcode', 'name', 'ebike'])

def nbSlotsVelibs(df): # Grouped by station code, number of emtpy velib slots available
  return df.select(['stationcode', 'name', 'numdocksavailable'])

def parseKafkaData(df, schema): # Return a parsed json string kafka df
  return df.select(from_json(col('value'), schema).alias('jsonData')).select('jsonData.*')
