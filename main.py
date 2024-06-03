from rabbitmq_manager import RabbitMQManager
from database_manager import mongodb
from datetime import timedelta
import datetime
import time
from email_manager import email_manager
from constant import MONGODB_URL_LIST, DATABASE_NAME_LIST

class main:
    def __init__(self) -> None:
        
        self.email_manager = email_manager()
        self.database_manager_dict = {}
        

    def create_object(self):
        self.rabbitmq_queue = RabbitMQManager()
        try:
            for url, name in zip(MONGODB_URL_LIST, DATABASE_NAME_LIST):
                self.database_manager_dict[url] = mongodb(url,name)
        except Exception as e:
            print(e)
            
    def check_queue_size(self):
        self.rabbitmq_queue.send_message()

    def check_status(self):
        self.current_time = datetime.datetime.now().second  # change second to min

        if self.current_time % 5 in [0, 5]:
            print("*"*5)
            print("5 min completed")
            for url in MONGODB_URL_LIST:
                print("#"*10)
                print(url)
                self.database_manager = self.database_manager_dict[url]

                
                
                if not self.database_manager.reconnect():
                    self.send_to_email("Database")

            
            
            
            # if not self.rabbitmq_queue.reconnect():
            #     self.send_to_email("RabbitMQ")
            # if not self.database_manager.reconnect():
            #     self.send_to_email("Database")


    def send_to_email(self,name):
        self.email_manager.send_email(name)
        

main = main()
main.create_object()

while True:
    main.check_status()

    time.sleep(1)
