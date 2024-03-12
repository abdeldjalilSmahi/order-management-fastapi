import json
import time

from business_logic_layer.message_queues import receveoir_message_a_queue, envoyer_message_a_queue
from business_logic_layer.models import CustomerBllModel
from business_logic_layer.businessrules import BusinessRulesCustomer, BusinessRulesProducts, BusinessRulesOrder
from business_logic_layer.order_verification import clear_console
from business_logic_layer.requests_customerside import send_confirmation
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    print(data)
    customer_id = data['customer_id']
    order_id = data['order_id']
    status = Status.get_status_by_name(data['status'])
    customer_bll_model = BusinessRulesCustomer.get_customer_by_id(int(customer_id))
    order_bll_model = BusinessRulesOrder.get_order_by_id(customer_bll_model, order_id)
    BusinessRulesOrder.update_status_order(order_bll_model, status)
    if status == Status.cancelled_by_customer:
        BusinessRulesOrder.termine_order(order_bll_model)
    else:
        BusinessRulesOrder.update_status_order(order_bll_model, Status.validated)
        # envoyer_message_a_queue('order_verifcation', data_to_send)  # message
        pass
    ch.basic_ack(delivery_tag=method.delivery_tag)
    time.sleep(10)
    print("*****************************************************************************************")



if __name__ == "__main__":
    receveoir_message_a_queue('customer_decision', on_message_received)
