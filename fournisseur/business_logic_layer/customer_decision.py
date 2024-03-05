import json
from business_logic_layer.message_queues import receveoir_message_a_queue, envoyer_message_a_queue
from business_logic_layer.models import CustomerBllModel
from business_logic_layer.businessrules import BusinessRulesCustomer, BusinessRulesProducts, BusinessRulesOrder
from business_logic_layer.requests_customerside import send_confirmation
from data_access_layer.models import Status


def on_message_received(ch, method, properties, body):
    data = json.loads(body)
    status = data.get('status')
    status = Status.get_status_by_name(status)
    order_id = int(data.get('order_id'))
    BusinessRulesOrder.update_status_order(order_id, status)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("*****************************************************************************************")


if __name__ == "__main__":
    receveoir_message_a_queue('place_order', on_message_received)
