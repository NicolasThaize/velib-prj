from kafka import KafkaProducer
import requests
from time import sleep
from json import dumps
from dateutil import parser
from datetime import datetime

KAFKA_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))

last_timestamp = {}

def get_velib_data(nrows=10, single_station=False): 
    # schedule the next call first
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=" + str(nrows) + "&sort=duedate" if not single_station else "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=9999&sort=duedate&facet=stationcode&refine.stationcode=25005"
    r = requests.get(url)
    # print(r.json()['records'][0])
    return r.json()

def date1_greater_date2(date1, date2):
    return date1 > date2

def parse_string_date(date_string, format):
    return datetime.strptime(date_string, format)

def convert_due_date_to_timestamp(date):
    return parser.parse(date).strftime(KAFKA_TIMESTAMP_FORMAT)

def store_to_kafka():
    while True:
        velibs_data = get_velib_data(nrows=9999)
        print("No of velibs stations: ", len(velibs_data['records']))
        for station_data in velibs_data['records']:
            station_data['fields']['duedate'] = convert_due_date_to_timestamp(station_data['fields']['duedate']) # Formatting date format to allow spark timestamp usage
            station_data['fields']['timestamp'] = station_data['fields'].pop('duedate')

            station_code = station_data['fields']['stationcode']
            station_last_refresh = station_data['fields']['timestamp']
        
            if station_code in last_timestamp: # If key already exist
                if date1_greater_date2(parse_string_date(station_last_refresh, KAFKA_TIMESTAMP_FORMAT), parse_string_date(last_timestamp[station_code], KAFKA_TIMESTAMP_FORMAT)): # If date from API is greater than kafka's last stored one
                    print(station_data['fields'], " UPDATED")
                    producer.send('test1', station_data['fields'])
                    last_timestamp[station_code] = station_last_refresh
            else: # If key does not exist
                print(station_data['fields'], " CREATED")
                producer.send('test1', station_data['fields'])
                last_timestamp[station_code] = station_last_refresh
        sleep(60)


store_to_kafka()
# get_velib_data(single_station=True)

#while True:
#    producer.send('test1', get_velib_data())
#    sleep(5)