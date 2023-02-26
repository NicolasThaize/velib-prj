import pymongo
from utils.envs import MONGO_DB_CONNECTION_STRING, MONGO_DB_NAME

class MongoForeachSinker:
    def __init__(self, collection):
        self.myclient = None
        self.mydb = None
        self.mycol = None
        self.collectionString = collection

    def open(self, partition_id, epoch_id):
        self.myclient = pymongo.MongoClient(MONGO_DB_CONNECTION_STRING)
        self.mydb = self.myclient[MONGO_DB_NAME]
        self.mycol = self.mydb[self.collectionString]
        return True

    def process(self, row):
        self.mycol.insert_one(row.asDict(recursive=True)) 
        pass

    def close(self, error):
        self.myclient.close()  
        pass