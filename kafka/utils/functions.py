from dateutil import parser
from datetime import date, timedelta
from utils.envs import KAFKA_TIMESTAMP_FORMAT
from datetime import datetime

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
