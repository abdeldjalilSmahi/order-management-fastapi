import json
from business_logic_layer.message_queues import receveoir_message_a_queue, envoyer_message_a_queue
from business_logic_layer.models import CustomerBllModel
from business_logic_layer.businessrules import BusinessRulesCustomer, BusinessRulesProducts, BusinessRulesOrder
from business_logic_layer.requests_customerside import send_confirmation
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    client = extract_customer(data)
    products = extract_products(data)
    if not BusinessRulesCustomer.verify_business_rules(client):
        message = "le client n'a pas rempli tous ses information correctement"
        print(message)
        customer_side_response = send_confirmation(customer_number=client.customer_number,
                                                   order_number=data.get('order_number'),
                                                   customer_id=None,
                                                   order_id=None
                                                   , email=data.get('email'),
                                                   status=Status.cancelled_by_seller,
                                                   decision=message)
        print(f"Customer side : {customer_side_response['message']}")
    if not BusinessRulesProducts.verify_products_names_and_positive_quantities(products):
        print("liste des produit invalides ou zero ou moins")
        # lancer processus d'annulation
    else:
        customer_bll_model, order_bll_model, products_quantities = valider_operation(data, client)
        if order_bll_model.actual_status == Status.cancelled_by_seller:
            print("Opération n'est pas validé par l'agent de fournisseur")
            print("Nous allons procéder à l'annulation de la commande par envoie au client")
            ## Rajouté!!
            message = "Opération non validée. Annulation de la commande."

            customer_side_response = send_confirmation(customer_number=customer_bll_model.customer_number,
                                                       order_number=order_bll_model.order_number,
                                                       customer_id=customer_bll_model.customer_id,
                                                       order_id=order_bll_model.order_id
                                                       , email=customer_bll_model.email, status=order_bll_model.actual_status,
                                                       decision=message)
            print(f"Customer side : {customer_side_response['message']}")
            new_status = Status.cancelled_and_finished
            order_bll_model = BusinessRulesOrder.update_status_order(order_bll_model, new_status)
            ## Rajouté !!
        else:
            data_to_next_step = {
                "customer_information": customer_bll_model.__dict__,
                "order_information": order_bll_model.to_dict(),
                "order_lines": products_quantities
            }
            data_to_send = json.dumps(data_to_next_step)
            envoyer_message_a_queue('order_verifcation', data_to_send)  # message
            print("Traitement terminé.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("*****************************************************************************************")


def extract_customer(data: dict):
    customer_number = data.get("customer_number")
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone_number = data.get('phone_number')
    customer_bll_model = CustomerBllModel(customer_number, firstname, lastname, email, phone_number)
    return customer_bll_model


def extract_products(data: dict):
    products = data.get('produits')
    return products


def valider_operation(data: dict, client: CustomerBllModel):
    print(f"INFORMATION DE LA COMMANDE:\n")

    try:
        customer_bll_model = CustomerBllModel(**BusinessRulesCustomer.add_customer(client))
        print(f"INFORMATION DE LA COMMANDE:\n")
        print(f"INFORMATION DE CLIENT:\n")
        print(customer_bll_model.__dict__)
        # order_bll_model = BusinessRulesOrder.get_last_order_initie_of_customer(customer_bll_model)
        order_number = int(data['order_number'])
        data_customer_number = data.get('customer_number')
        # if data_customer_number != customer_bll_model.customer_number:
        #     BusinessRulesCustomer.update_customer_number(customer_bll_model, customer_bll_model.customer_number)
        order_bll_model = BusinessRulesOrder.add_order(customer_bll_model, order_number)
        print(f"INFORMATION DE LA COMMANDE:\n")
        print(order_bll_model.to_dict())
        print(data.get("produits"))

        while True:
            decision = input("Les informations du client sont valides, tu valides l'opération ? (oui/non) ").strip() \
                .lower()
            if decision in ["oui", "ok", "valide"]:
                new_status = Status.processing
                message = "Opération validée. Passage à la prochaine étape."
                break
            elif decision in ["non", "no", "pas", "valide pas"]:
                new_status = Status.cancelled_by_seller
                BusinessRulesOrder.update_status_order(order_bll_model, new_status)
                message = "Opération non validée. Annulation de la commande."
                # customer_side_response = send_confirmation(customer_number=customer_bll_model.customer_number,
                #                                            order_number=order_number,
                #                                            customer_id=customer_bll_model.customer_id,
                #                                            order_id=order_bll_model.order_id
                #                                            , email=customer_bll_model.email, status=new_status,
                #                                            decision=message)
                # print(customer_side_response['message'])
                # new_status = Status.cancelled_and_finished
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
