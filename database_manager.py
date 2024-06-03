# from constant import MONGODB_URL,DATABASE_NAME
from datetime import timedelta
from pymongo import MongoClient

class mongodb:
    def __init__(self, MONGODB_URL, DATABASE_NAME):
        self.mongo_url = MONGODB_URL
        self.database_name=DATABASE_NAME
        try:
            self.myclient = MongoClient(self.mongo_url)
            self.mydb = self.myclient[self.database_name]
        except:
            print("MongoDB not connected")
            
    def reconnect(self):
        connected = False
        try:
            self.myclient = MongoClient(self.mongo_url)
            self.mydb = self.myclient[self.database_name]
            self.enter("test",{"hello":"world"})
            connected = True
        except:
            print("MongoDB not connected")
        print(connected,self.mongo_url,self.database_name)
        return connected

    # enter values in database
    def enter(self, name, data):
        self.mycollection = self.mydb[name]
        self.mycollection.insert_one(data)
        