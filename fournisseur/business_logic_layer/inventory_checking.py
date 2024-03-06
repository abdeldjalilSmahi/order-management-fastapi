import json
from datetime import datetime

from business_logic_layer.message_queues import receveoir_message_a_queue, envoyer_message_a_queue
from business_logic_layer.models import CustomerBllModel, OrderBllModel
from business_logic_layer.requests_customerside import send_confirmation
from data_access_layer.dataaccess import DataAccessorTransaction
from business_logic_layer.businessrules import BusinessRulesProducts, BusinessRulesOrder, BusinessRulesOrderLines
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    customer_bll_model = CustomerBllModel(**data['customer_information'])
    order_bll_model = data['order_information']
    order_lines = data['order_lines']
    #################################
    business_rules_order = BusinessRulesOrder.construct_order_bll_model_factory(customer_bll_model, order_bll_model,
                                                                                order_lines)
    ###################
    boolean, status, message, business_rules_order = valider_operation_(business_rules_order)
    customer_side_message = send_confirmation(customer_number=customer_bll_model.customer_number,
                                              order_number=order_bll_model.get('order_number'),
                                              customer_id=customer_bll_model.customer_id,
                                              email=customer_bll_model.email,
                                              status=status, decision=message, order_id=order_bll_model.get('order_id'))
    print({"customer_side_message": customer_side_message})

    if boolean:
        data_to_send = business_rules_order.to_dict()
        print(data_to_send)
        envoyer_message_a_queue('inventory_checking', json.dumps(data_to_send))  # message
        print("Traitement terminé. Passage à la gestion de devis")

    else:
        ## PAss au suivant ## Annulation deja fait dans le code de la validation !
        print("Traitement terminé. Commande annulée !")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("*****************************************************************************************")


def construct_order_bll_model(customer_bll_model, order_bll_model):
    order_bll_model["actual_status"] = Status.get_status_by_name(order_bll_model["actual_status"])
    order_bll_model["order_date"] = datetime.strptime(order_bll_model["order_date"], "%Y-%m-%dT%H:%M:%S")
    order_bll_model["customer"] = customer_bll_model
    return OrderBllModel(**order_bll_model)


def valider_operation_(business_rules_order: BusinessRulesOrder):
    try:
        order_lines = business_rules_order.order_lines
        order_bll_model_information = business_rules_order.order  ## BLL MODEL
        customer_bll_model_information = business_rules_order.customer  ##BLL MODEL
        ############################
        order_bll_model = BusinessRulesOrder.get_order_by_id(customer_bll_model_information, order_bll_model_information
                                                             .order_id)
        cancel_cases = [
            Status.cancelled_and_finished
        ]
        ### DEBUT FIRST CASE
        if order_bll_model.actual_status in cancel_cases:
            message = "Cette commande a été deja cloturée"
            print(message)
            return False, order_bll_model.actual_status, message, business_rules_order
        ### FIN FIRST CASE
        ### DEBUT SECONDE CASE
        if order_bll_model.actual_status == Status.on_hold:
            print("Cette commande a déjà été vérifiée et mise en pause.")
            print(
                "La quantité est suffisante, réservation en cours des produits pour le client. La commande est mise en "
                "pause jusqu'à confirmation.")
            order_bll_model_information = order_bll_model
            print_information(customer_bll_model_information, order_bll_model_information, order_lines)
            boolean, status, message, business_rules_order = validation_manuelle_operation(business_rules_order)
            return boolean, status, message, business_rules_order
        ### FIN SECONDE CASE
        ### DEBUT THIRD CASE VERIFICATION STOCK
        print_information(customer_bll_model_information, order_bll_model_information, order_lines)
        verification, motif = BusinessRulesProducts.verify_inventory_quantities(order_lines)
        if not verification:
            ##Stock insuffisant
            print(motif)
            print("Lancement de l'annulation de la commande")
            business_rules_order.cancel_order()
            return False, Status.cancelled_by_seller, motif, business_rules_order

        print("La quantité est suffisante, réservation en cours des produits pour le client. La commande est mise en "
              "pause jusqu'à confirmation.")

        if order_bll_model_information.order_id is None:
            raise ValueError("Order ID manquant dans order_bll_model_information")

        for product_name, quantity_ordered in order_lines.items():
            product = BusinessRulesProducts.get_product_by_name(product_name)  ##BLL MODEL
            BusinessRulesOrderLines.add_order_line(order_bll_model_information, product, quantity_ordered)
        business_rules_order.update_order_status(Status.on_hold)
        boolean, status, message, business_rules_order = validation_manuelle_operation(business_rules_order)
        return boolean, status, message, business_rules_order

    except Exception as e:
        print(f"Une erreur est survenue: {e}")


def validation_manuelle_operation(business_rules_order: BusinessRulesOrder):
    while True:
        decision = input("Valider l'opération et passer à la génération de devis ? (oui/non) ").lower().strip()
        if decision in ["oui", "ok", "valide"]:
            business_rules_order.update_order_status(Status.processing)
            print("Opération validée. Passage à la génération de devis.")
            message = "Votre Commande a été Validé, vous recevez très prochainement votre devis !"
            return True, Status.validated, message, business_rules_order
        elif decision in ["non", "no", "pas", "valide pas"]:
            business_rules_order.update_order_status(Status.cancelled_by_seller)
            print(business_rules_order.get_order_by_id(business_rules_order.customer,
                                                       business_rules_order.order.order_id).actual_status.value)
            business_rules_order.cancel_order()
            print("Opération non validée. Annulation de la commande.")
            return (False, Status.cancelled_by_seller, "Opération non validée. Annulation de la commande."
                    , business_rules_order)
        else:
            print("Entrée invalide. Veuillez répondre par 'oui' ou 'non'.")


def print_information(customer, order_information, order_lines):
    print("*****************************************************************************************")
    print(f"CUSTOMER INFORMATION:\n{json.dumps(customer.__dict__, indent=4)}")
    print("*****************************************************************************************")
    print(f"ORDER INFORMATION:\n{json.dumps(order_information.to_dict(), indent=4)}")
    print("*****************************************************************************************")
    print(f"ORDER LINES INFORMATION:\n{json.dumps(order_lines, indent=4)}")
    print("*****************************************************************************************")


if __name__ == "__main__":
    receveoir_message_a_queue('order_verifcation', on_message_received)
