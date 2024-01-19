from fastapi import FastAPI, BackgroundTasks
import pika
import json
import threading

app = FastAPI()

def envoyer_message_a_queue(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ma_queue')
    channel.basic_publish(exchange='', routing_key='ma_queue', body=message)
    channel.close()
    connection.close()

def verifier_commande():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ma_queue')

    for method_frame, properties, body in channel.consume('ma_queue'):
        print("Commande reçue et en cours de traitement:", body)
        channel.basic_ack(method_frame.delivery_tag)
        if body == 'quit':
            break

    channel.cancel()
    channel.close()
    connection.close()

@app.post("/envoyer_commande/")
async def envoyer_commande(commande: dict, background_tasks: BackgroundTasks):
    commande_json = json.dumps(commande)
    background_tasks.add_task(envoyer_message_a_queue, commande_json)
    return {"message": "Commande en cours d'envoi"}

# Démarrage du consommateur dans un thread séparé
threading.Thread(target=verifier_commande, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
