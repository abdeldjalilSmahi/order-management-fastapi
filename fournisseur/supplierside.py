import threading

from fastapi import FastAPI, HTTPException, BackgroundTasks, Body
from models.models import CommandeModel, Commande
import pika
import json

app = FastAPI()


@app.post("/place_order")
async def place_order(backgroundtasks: BackgroundTasks, commande: CommandeModel = Body()):
    description = commande.description
    # commande = Commande(description=description)
    message = "test"
    backgroundtasks.add_task(envoyer_message_a_queue, message)
    return {"message": "Votre commande a été bien reçu"}


def envoyer_message_a_queue(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ma_queue')
    channel.basic_publish(exchange='', routing_key='ma_queue', body=message)
    channel.close()
    connection.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
