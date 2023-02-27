from kafka import KafkaConsumer

import csv
from datetime import date
import os.path
import json

CSV_FOLDER_PATH = "../consumed_csv/"

consumer = KafkaConsumer('test1', bootstrap_servers='localhost:9092')

for msg in consumer:
    station_dict = json.loads(msg.value.decode('utf-8'))
    
    today_date = date.today().strftime("%d_%m_%Y")
    csv_name = "velib_raw_data_" + today_date + ".csv"
    csv_file_path = CSV_FOLDER_PATH + csv_name

    #test if file exists
    file_exist = os.path.isfile(csv_file_path)
    if not os.path.exists(CSV_FOLDER_PATH):
        os.makedirs(CSV_FOLDER_PATH)
    
    with open(csv_file_path, mode='a', newline='\n', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        
        if not file_exist:
            writer.writerow(list(station_dict.keys()))
        writer.writerow(station_dict.values())