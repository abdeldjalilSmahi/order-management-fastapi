import datetime
import json

from business_logic_layer.businessrules import BusinessRulesProducts, BusinessRulesOrder
from business_logic_layer.message_queues import receveoir_message_a_queue
from business_logic_layer.models import CustomerBllModel, OrderBllModel
from business_logic_layer.requests_customerside import send_confirmation, send_devis
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    customer = data['customer']
    customer_bll_model = CustomerBllModel(**customer)
    order = data['order']
    order['order_date'] = datetime.datetime.fromisoformat(order['order_date'])
    order['actual_status'] = Status(order['actual_status'])
    order_bll_model = OrderBllModel(**order, customer=customer_bll_model)
    order_lines = data['order_lines']
    print("*****************************************************************************************")
    business_rules_order = BusinessRulesOrder(customer_bll_model, order_bll_model, order_lines)
    print(business_rules_order.to_dict())
    print("*****************************************************************************************")
    devis = generate_devis(business_rules_order, order_lines)
    boolean, message, business_rules_order = valider_operation(devis, business_rules_order)
    customer_side_message = send_devis(devis, business_rules_order.customer.customer_number)
    print(customer_side_message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("*****************************************************************************************")


def valider_operation(devis: dict, business_rules_order: BusinessRulesOrder):
    print(devis)
    return validation_manuelle_operation(business_rules_order)


def validation_manuelle_operation(business_rules_order: BusinessRulesOrder):
    while True:
        decision = input("Validez vous le devis ? (oui/non) ").lower().strip()
        if decision in ["oui", "ok", "valide"]:
            business_rules_order.update_order_status(Status.awaiting_confirmation)
            print("Opération validée. Passage à l'envoie du devis.")
            message = "Vous trouvez ci joint le devis !"
            return True, message, business_rules_order
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


def generate_devis(business_rules_order: BusinessRulesOrder, order_lines: dict):
    tva = 0.1
    total = 0
    devis = {
        "order_number": business_rules_order.order.order_number,
        "customer_id": business_rules_order.customer.customer_id,
        "order_id": business_rules_order.order.order_id,
        "products": {},
        "total_price": 0
    }

    for product in order_lines:
        product_bll_model = BusinessRulesProducts.get_product_by_name(product)
        product_unit_price = product_bll_model.unit_price
        quantity_ordered = order_lines[product]
        total_by_product = (product_unit_price * quantity_ordered) + (product_unit_price * quantity_ordered * tva)
        devis["products"][product] = {"unit_price": product_unit_price,
                                      "quantity_ordered": quantity_ordered,
                                      "tva_rate": tva
                                      }
        total += total_by_product
        devis['total_price'] = total
    return devis


if __name__ == "__main__":
    receveoir_message_a_queue('inventory_checking', on_message_received)
    # # generate_devis({"product1": 2, "product2":5})
    # data = {'customer': {'customer_id': 4, 'customer_number': '59a252f3e1ab44648f93a89374bab38f', 'firstname': 'ishak',
    #                      'lastname': 'amine', 'email': 'a.i@temp.com', 'phone_number': '0764177193'},
    #         'order': {'order_id': 21, 'order_number': 6, 'order_date': '2024-03-03T16:20:43', 'customer_id': 4,
    #                   'actual_status': 'Processing'}, 'order_lines': {'product2': 9, 'product1': 2}}
    #
    # customer = data['customer']
    # customer_bll_model = CustomerBllModel(**customer)
    # order = data['order']
    # order['order_date'] = datetime.datetime.fromisoformat(order['order_date'])
    # order['actual_status'] = Status(order['actual_status'])
    # order_bll_model = OrderBllModel(**order, customer=customer_bll_model)
    # order_lines = data['order_lines']
    # busines_rules_prder = BusinessRulesOrder(customer_bll_model, order_bll_model, order_lines)
    # print(busines_rules_prder.to_dict())
