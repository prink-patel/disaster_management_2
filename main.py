from rabbitmq_manager import RabbitMQManager
from database_manager import mongodb
from datetime import timedelta
import datetime
import time
from email_manager import email_manager
from constant import MONGODB_LIST,RABBITMQ_LIST

class main:
    def __init__(self) -> None:
        
        self.email_manager = email_manager()
        self.database_manager_dict = {}
        self.rabbitmq_manager_dict = {}
        

    def create_object(self):
        # self.rabbitmq_queue = RabbitMQManager()
        try:
            for data in MONGODB_LIST:
                self.database_manager_dict[data["MONGODB_URL"]] = mongodb(data["MONGODB_URL"],data["DATABASE_NAME"])
            
            for data in RABBITMQ_LIST:
                self.rabbitmq_manager_dict[data["RABBITMQ_USERNAME"]] = RabbitMQManager(data)
                
                
                
                
        except Exception as e:
            print(e)
            
    def check_queue_size(self):
        self.rabbitmq_queue.send_message()

    def check_status(self):
        self.current_time = datetime.datetime.now().second  # change second to min
        if self.current_time % 5 in [0, 5]:
            print("*"*5)
            print("5 min completed")
            
            for data in MONGODB_LIST:
                self.database_manager = self.database_manager_dict[data["MONGODB_URL"]]
                if not self.database_manager.reconnect():
                    self.send_to_email(f"Database {data['MONGODB_URL']}")

            for data in RABBITMQ_LIST:
                self.rabbitmq_manager = self.rabbitmq_manager_dict[data["RABBITMQ_USERNAME"]]
                if not self.rabbitmq_manager.reconnect():
                    self.send_to_email(f"RabbitMQ {data['RABBITMQ_USERNAME']}")

    def send_to_email(self,name):
        self.email_manager.send_email(name)
        

main = main()
main.create_object()

while True:
    main.check_status()

    time.sleep(1)
