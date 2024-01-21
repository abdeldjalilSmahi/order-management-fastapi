import pika


def envoyer_message_a_queue(queue_name: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    channel.close()
    connection.close()


def receveoir_message_a_queue(queue_name: str, methode_a_executer: callable):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=methode_a_executer)
    print("Début de la consommation des messages.")
    channel.start_consuming()
