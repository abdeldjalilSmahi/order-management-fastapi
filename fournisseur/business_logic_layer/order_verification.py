import json
from business_logic_layer.message_queues import receveoir_message_a_queue, envoyer_message_a_queue
from business_logic_layer.models import CustomerBllModel
from business_logic_layer.businessrules import BusinessRulesCustomer, BusinessRulesProducts, BusinessRulesOrder
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    client = extract_customer(data)
    products = extract_products(data)
    if not BusinessRulesCustomer.verify_business_rules(client):
        print("le client n'a pas rempli tous ses information correctement")
        # lancer le processus l'annulation de la commande
    if not BusinessRulesProducts.verify_products_names_and_positive_quantities(products):
        print("liste des produit invalides ou zero ou moins")
        # lancer processus d'annulation

    else:
        customer_bll_model, order_bll_model, products_quantities = valider_operation(data, client)
        if order_bll_model.actual_status == Status.cancelled_by_seller:
            print("Opération n'est pas validé par l'agent de fournisseur")
            print("Nous allons procéder à l'annulation de la commande par envoie au client")
            # Suppression de la commande
        else:
            data_to_next_step = {
                "customer_information": customer_bll_model.__dict__,
                "order_information": order_bll_model.to_dict(),
                "order_lines": products_quantities
            }
            data_to_send = json.dumps(data_to_next_step)
            envoyer_message_a_queue('order_verifcation', data_to_send) # message
            print("Traitement terminé.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("*****************************************************************************************")


def extract_customer(data: dict):
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone_number = data.get('phone_number')
    customer_bll_model = CustomerBllModel(firstname, lastname, email, phone_number)
    return customer_bll_model


def extract_products(data: dict):
    products = data.get('produits')
    return products


def valider_operation(data: dict, client: CustomerBllModel):
    print(f"INFORMATION DE LA COMMANDE:\n{json.dumps(data,indent=4)}")

    try:
        customer_bll_model = CustomerBllModel(**BusinessRulesCustomer.add_customer(client))
        order_bll_model = BusinessRulesOrder.get_last_order_initie_of_customer(customer_bll_model)

        order_bll_model = BusinessRulesOrder.add_order(customer_bll_model)
        order_id = order_bll_model.order_id

        while True:
            decision = input("Les informations du client sont valides, tu valides l'opération ? (oui/non) ").strip()\
                .lower()
            if decision in ["oui", "ok", "valide"]:
                new_status = Status.processing
                message = "Opération validée. Passage à la prochaine étape."
                break
            elif decision in ["non", "no", "pas", "valide pas"]:
                new_status = Status.cancelled_by_seller
                BusinessRulesOrder.update_status_order(order_bll_model, new_status)
                new_status = Status.cancelled_and_finished
                message = "Opération non validée. Annulation de la commande."
                break
            else:
                print("Entrée invalide. Veuillez répondre par 'oui' ou 'non'.")

        order_bll_model = BusinessRulesOrder.update_status_order(order_bll_model, new_status)
        products_quantities = data.get("produits")

        print(message)
        return customer_bll_model, order_bll_model, products_quantities

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        # Optionnellement, vous pouvez gérer ou propager l'exception ici


if __name__ == "__main__":
    receveoir_message_a_queue('place_order', on_message_received)
