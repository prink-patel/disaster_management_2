import pika
import time
import random
from queue import Queue


class RabbitMQManager:

    def __init__(self,RABBITMQ_DATA):
        # logger.info(f"RabbitMQManager Called")
        self.rabbitmq_data = RABBITMQ_DATA
        # Queue to store msgs
        self.rabbitmq_queue = Queue(maxsize=500)
        self.running = True

        # RabbitMQ Connection
        self.credentials = pika.PlainCredentials(self.rabbitmq_data["RABBITMQ_USERNAME"],self.rabbitmq_data["RABBITMQ_PASSWORD"])
        self.parameters = pika.ConnectionParameters(
            self.rabbitmq_data["RABBITMQ_HOST"], credentials=self.credentials
        )

    def reconnect(self):
        connected = False
        time.sleep(1)
        try:
            # logger.info("Reconnecting and publishing")
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            connected = True
        except Exception:
            # logger.info(f"Exception in reconnect_and_publish {traceback.print_exc()}")
            time.sleep(0.1)
            pass
        return connected


    def message_count(self):
        return False
    

    def check_queue_lenght(self):
        try:
            self.queue = self.channel.queue_declare(queue=self.rabbitmq_data["RABBIT_QUEUE_NAME"], passive=True)
            self.channel.queue_bind(queue=self.queue.method.queue, exchange=self.rabbitmq_data["RABBIT_EXCHANGE_NAME"], routing_key=self.rabbitmq_data["RABBIT_ROUTING_KEY"])
            message_count = self.queue.method.message_count

            if message_count >= self.rabbitmq_data["RABBIT_QUEUE_MAX_SIZE"]:
                return True
        except Exception as e:
            print("1")
            return True
