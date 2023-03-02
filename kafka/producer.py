from kafka import KafkaProducer
from time import sleep
from json import dumps

from utils.envs import KAFKA_TIMESTAMP_FORMAT
from utils.functions import date1_greater_date2, convert_due_date_to_timestamp, parse_string_date, \
    is_due_date_valid, get_velib_data, get_last_timestamp_dict, get_velib_data_offline, write_last_timestamp

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))

IS_OFFLINE=False

def store_to_kafka(offline=False): # main
    while True:
        last_timestamp = get_last_timestamp_dict()

        velibs_data = get_velib_data_offline() if offline else get_velib_data(nrows=9999) # Get velib's raw data
        velibs_data_filtered = list(filter(is_due_date_valid, velibs_data['records'])) # Filtering station records that already has been stored to kafka topic
        for station_data in velibs_data_filtered: # For each velib station
            station_data['fields']['duedate'] = convert_due_date_to_timestamp(station_data['fields']['duedate']) # Formatting date format to allow spark timestamp usage
            station_data['fields']['timestamp'] = station_data['fields'].pop('duedate') # Renaming 'duedate' column to 'timestamp'
            station_code = station_data['fields'].get('stationcode')
            if station_code is None: # To prevent stationcode KeyError
                continue
            station_last_refresh = station_data['fields']['timestamp']
            
            if station_code in last_timestamp: # If key already exist
                if date1_greater_date2(parse_string_date(station_last_refresh, KAFKA_TIMESTAMP_FORMAT), parse_string_date(last_timestamp[station_code], KAFKA_TIMESTAMP_FORMAT)): # If date from API is greater than kafka's last stored one
                    print(station_data['fields']['stationcode'], " UPDATED")
                    producer.send('stations_raw_data', station_data['fields'])
                    last_timestamp[station_code] = station_last_refresh # Update last station timestamp field
            else: # If key does not exist
                print(station_data['fields']['stationcode'], " CREATED")
                producer.send('stations_raw_data', station_data['fields'])
                last_timestamp[station_code] = station_last_refresh # Create last station timestamp field
        
        write_last_timestamp(last_timestamp)
        sleep(60) # Refresh data every minutes

store_to_kafka(offline=IS_OFFLINE)
