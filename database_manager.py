# from constant import MONGODB_URL,DATABASE_NAME
from datetime import timedelta
from pymongo import MongoClient
from pprint import pprint

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
            self.check_camera_alive()
            connected = True

        except:
            print("MongoDB not connected")
        print(connected,self.mongo_url,self.database_name)
        return connected
    
    def check_camera_alive(self):
        pipeline = [
            {"$group": {"_id": "$camera_name", "max_time": {"$max": "$event_time"}}}
        ]
        data = self.mydb["occupancy"].aggregate(pipeline)
        pprint(data)

        