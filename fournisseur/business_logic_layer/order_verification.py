import json
from business_logic_layer.message_queues import receveoir_message_a_queue
from business_logic_layer.models import CustomerBllModel
from data_access_layer.dataaccess import DataAccessCustomer


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    client = extract_customer(data)
    if not client.is_valid():
        print("le client n'a pas rempli tous ses information correctement")
        # lancer l'annulation de la commande
    else:
        print("client valide")
        valider_operation(client)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Traitement terminé.")


def extract_customer(data: dict):
    firstname = data.pop('firstname')
    lastname = data.pop('lastname')
    email = data.pop('email')
    phone_number = data.pop('phone_number')
    client = CustomerBllModel(firstname, lastname, email, phone_number)
    return client


def valider_operation(client: CustomerBllModel):
    print(client.__dict__)
    decision = str(input("les informations du client sont valide, tu valides l'opération ? ")).lower()
    match decision:
        case "oui" | "ok" | "valide":
            print("operation validé")
            DataAccessCustomer.add_customer(client)
            #
        case "non" | "no" | "pas" | "valide pas":
            print("operation non validé")
        case _:
            valider_operation(client)


if __name__ == "__main__":
    receveoir_message_a_queue('place_order', on_message_received)
