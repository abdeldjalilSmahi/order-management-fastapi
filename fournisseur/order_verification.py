import pika


def on_message_received(ch, method, properties, body):
    print(f"Reçu {body}, traitement en cours, durée estimée .")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Traitement terminé.")


def verifier_commande():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ma_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='ma_queue', on_message_callback=on_message_received)
    print("Début de la consommation des messages.")
    channel.start_consuming()


if __name__ == "__main__":
    verifier_commande()
