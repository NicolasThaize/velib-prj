from kafka import KafkaProducer
import requests
from time import sleep
from json import dumps, load

from utils.envs import KAFKA_TIMESTAMP_FORMAT
from utils.functions import date1_greater_date2, convert_due_date_to_timestamp, parse_string_date, \
    is_due_date_valid

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))

LAST_TIMESTAMP = {}
IS_OFFLINE=False

def get_velib_data(nrows=10, single_station=False): # HTTP GET on api endpoint according to number of rows requested
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=" + str(nrows) + "&sort=duedate" if not single_station else "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=9999&sort=duedate&facet=stationcode&refine.stationcode=25005"
    r = requests.get(url)
    return r.json() # return the json content of the response

def get_velib_data_offline():
    with open('/Users/nicolas/Documents/Cours/M1/Big data/Projet velib/velib-prj/kafka/raw_data.json') as json_string:
        return load(json_string)

def filter_outdated_data(df):
    return df.filter()

def store_to_kafka(offline=False): # main
    while True:
        velibs_data = get_velib_data_offline() if offline else get_velib_data(nrows=9999) # Get velib's raw data
        print("No of velibs stations: ", len(velibs_data['records']))
        velibs_data_filtered = list(filter(is_due_date_valid, velibs_data['records']))
        for station_data in velibs_data_filtered: # For each velib station
            station_data['fields']['duedate'] = convert_due_date_to_timestamp(station_data['fields']['duedate']) # Formatting date format to allow spark timestamp usage
            station_data['fields']['timestamp'] = station_data['fields'].pop('duedate') # Renaming 'duedate' column to 'timestamp'
            station_code = station_data['fields']['stationcode']
            station_last_refresh = station_data['fields']['timestamp']
            if station_code in LAST_TIMESTAMP: # If key already exist
                if date1_greater_date2(parse_string_date(station_last_refresh, KAFKA_TIMESTAMP_FORMAT), parse_string_date(LAST_TIMESTAMP[station_code], KAFKA_TIMESTAMP_FORMAT)): # If date from API is greater than kafka's last stored one
                    print(station_data['fields']['stationcode'], " UPDATED")
                    producer.send('test1', station_data['fields'])
                    LAST_TIMESTAMP[station_code] = station_last_refresh # Update last station timestamp field
            else: # If key does not exist
                print(station_data['fields']['stationcode'], " CREATED")
                producer.send('test1', station_data['fields'])
                LAST_TIMESTAMP[station_code] = station_last_refresh # Create last station timestamp field
        sleep(60) # Refresh data every minutes


store_to_kafka(offline=IS_OFFLINE)
