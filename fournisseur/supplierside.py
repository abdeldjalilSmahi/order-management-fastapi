from fastapi import FastAPI, HTTPException, BackgroundTasks

import pika
from threading import Lock

class RabbitMQConnectionSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(RabbitMQConnectionSingleton, cls).__new__(cls)
                # Initialisation de la connexion RabbitMQ
                cls._instance.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                cls._instance.channel = cls._instance.connection.channel()
        return cls._instance

    def get_channel(self):
        return self._instance.channel

    def close_connection(self):
        if self._instance.connection:
            self._instance.connection.close()
            self._instance = None


# Récupération de la connexion RabbitMQ
rabbitmq_connection = RabbitMQConnectionSingleton()
channel = rabbitmq_connection.get_channel()

# Utilisation de la connexion (par exemple, déclarer une queue)
channel.queue_declare(queue='ma_queue')

app = FastAPI()

@app.post("/place_order")
async def place_order():
    pass