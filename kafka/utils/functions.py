from dateutil import parser
from datetime import datetime
from utils.envs import KAFKA_TIMESTAMP_FORMAT

def date1_greater_date2(date1, date2): # Returns True if date1 is greater than date2, False otherwise
    return date1 > date2

def parse_string_date(date_string, format): # Parse a string date to a specified format
    return datetime.strptime(date_string, format)

def convert_due_date_to_timestamp(date): # Convert a string date to a specific formatted date
    return parser.parse(date).strftime(KAFKA_TIMESTAMP_FORMAT)