KAFKA_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
LAST_TIMESTAMP_FILE_PATH = './last_timestamp.json'
VELIB_REST_API_URL = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows={}&sort=duedate"
VELIB_SINGLE_STATION_REST_API_URL = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&lang=fr&rows=9999&sort=duedate&facet=stationcode&refine.stationcode=25005"