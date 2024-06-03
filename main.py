from rabbitmq_manager import RabbitMQManager
from database_manager import mongodb
from datetime import timedelta
import datetime
import time
from email_manager import email_manager


class main:
    def __init__(self) -> None:
        self.rabbitmq_queue = RabbitMQManager()
        self.database_manager = mongodb()
        self.email_manager = email_manager()
        self.rabbitmq_status_list = []
        self.database_status_list = []
        self.email_manager_counter_database = 0
        self.email_manager_counter_rabbit = 0

    def check_queue_size(self):
        self.rabbitmq_queue.send_message()

    def check_status(self):
        self.current_time = datetime.datetime.now().second  # change second to min

        if self.current_time % 5 in [0, 5]:
            print("5 min completed")
            if not self.rabbitmq_queue.reconnect():
                self.send_to_email("RabbitMQ")
            if not self.database_manager.reconnect():
                self.send_to_email("Database")


    def send_to_email(self,name):
        self.email_manager.send_email(name)
        

main = main()

while True:
    main.check_status()

    time.sleep(1)
