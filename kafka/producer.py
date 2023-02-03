from kafka import KafkaProducer
import requests
from time import sleep
from json import dumps, loads
from dateutil import parser

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


def store_to_kafka():
    while True:
        velibs_data = get_velib_data(nrows=9999)
        print("No of velibs stations: ", len(velibs_data['records']))
        for station_data in velibs_data['records']:
            station_code = station_data['fields']['stationcode']
            station_last_refresh = station_data['fields']['duedate']
        
            if station_code in last_timestamp: # If key already exist
                if date1_greater_date2(parser.parse(station_last_refresh), parser.parse(last_timestamp[station_code])): # If date from API is greater than kafka's last stored one
                    print(station_code, " UPDATED")
                    producer.send('test1', station_data)
                    last_timestamp[station_code] = station_last_refresh
            else: # If key does not exist
                print(station_code, " CREATED")
                producer.send('test1', station_data)
                last_timestamp[station_code] = station_last_refresh
        print(last_timestamp)
        sleep(60)


store_to_kafka()
# get_velib_data(single_station=True)

#while True:
#    producer.send('test1', get_velib_data())
#    sleep(5)