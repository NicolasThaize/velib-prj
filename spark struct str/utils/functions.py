from pyspark.sql.functions import col, from_json

def maxMechaVelibs(df): # Grouped by station code, number of mechanical velibs available
  return df.select(['stationcode', 'name', 'mechanical'])

def maxElecVelibs(df): # Grouped by station code, number of electrical velibs available
  return df.select(['stationcode', 'name', 'ebike'])

def nbSlotsVelibs(df): # Grouped by station code, number of emtpy velib slots available
  return df.select(['stationcode', 'name', 'numdocksavailable'])

def parseKafkaData(df, schema): # Return a parsed json string kafka df
  return df.select(from_json(col('value'), schema).alias('jsonData')).select('jsonData.*')
