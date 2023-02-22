from dateutil import parser
from datetime import date, timedelta
from utils.envs import KAFKA_TIMESTAMP_FORMAT, LAST_TIMESTAMP_FILE_PATH, VELIB_REST_API_URL, VELIB_SINGLE_STATION_REST_API_URL
from datetime import datetime
from json import dumps, load
from os import path
import requests

def get_today_date():
    return date.today()

def get_time_delta(days=0, hours=0, minutes=0):
    return timedelta(days=days, hours=hours, minutes=minutes)

def is_due_date_valid(station_data):
    ref_date = subtract_timedelta_to_date(get_time_delta(days=7), get_today_date())
    tested_date = convert_string_to_date(station_data['fields']['duedate']).date()
    return ref_date < tested_date

def subtract_timedelta_to_date(timedelta, date):
    return date - timedelta

def date1_greater_date2(date1, date2): # Returns True if date1 is greater than date2, False otherwise
    return date1 > date2

def parse_string_date(date_string, format): # Parse a string date to a specified format
    return datetime.strptime(date_string, format)

def convert_due_date_to_timestamp(date): # Convert a string date to a specific formatted date
    return parser.parse(date).strftime(KAFKA_TIMESTAMP_FORMAT)

def convert_string_to_date(date_string):
    return parser.parse(date_string)

def write_last_timestamp(dict):
    with open(LAST_TIMESTAMP_FILE_PATH, 'w') as convert_file:
        convert_file.write(dumps(dict))

def last_timestamp_dict_from_file():
    with open(LAST_TIMESTAMP_FILE_PATH) as json_file:
        return load(json_file)

def get_velib_data(nrows=10, single_station=False): # HTTP GET on api endpoint according to number of rows requested
    url = VELIB_REST_API_URL.format(nrows) if not single_station else VELIB_SINGLE_STATION_REST_API_URL
    r = requests.get(url)
    return r.json() # return the json content of the response

def get_velib_data_offline():
    with open('./kafka/raw_data.json') as json_string:
        return load(json_string)

def get_last_timestamp_dict():
    if path.isfile(LAST_TIMESTAMP_FILE_PATH): # If timestamp file exists
            return last_timestamp_dict_from_file() # Return last timestamp dict that was stored in the file
    else:
        return {} # Return empty dit