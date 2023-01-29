from kafka import KafkaProducer
import requests
from time import sleep
from json import dumps

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))

def get_velib_data(nrows=10): 
    # schedule the next call first
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=" + str(nrows) + "&sort=duedate&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    r = requests.get(url)
    return r.json()

while True:
    producer.send('test1', get_velib_data())
    sleep(5)