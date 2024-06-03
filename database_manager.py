# from constant import MONGODB_URL,DATABASE_NAME
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
from email_manager import email_manager

class mongodb:
    def __init__(self, MONGODB_URL, DATABASE_NAME):
        self.mongo_url = MONGODB_URL
        self.database_name=DATABASE_NAME
        self.email_manager = email_manager()
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
        dead_cameras = []
        
        pipeline = [
            {"$group": {"_id": "$camera_name", "last_entry": {"$max": "$event_time"}}},
        ]

        cameras = self.mydb.get_collection("occupancy").aggregate(pipeline)
        for camera in cameras:
            dead_since = (datetime.utcnow()-camera['last_entry']).total_seconds()/60
            if dead_since>5:
                dead_cameras.append({"camera_name":camera['_id'],"dead_since":dead_since})
        
        if len(dead_cameras)>0:
            body = f"Dead cameras: \n" + ',\n'.join(list(map(lambda x: x['camera_name'],dead_cameras)))
            self.email_manager.send_email(body)    

        