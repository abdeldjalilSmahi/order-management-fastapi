"""
Ce fichier, définit le processus d'annulation d'une commande par le fournisseur.
"""
from data_access_layer.models import Status
from data_access_layer.dataaccess import DataAccessOrders
import requests


def send_confirmation(customer_number: str,
                      order_number: int, customer_id, order_id, email: str, status: Status, decision: str):
    message_request = {
        "order_number": order_number,
        "customer_id": customer_id,
        "order_id": order_id,
        "email": email,
        "status": status.value,
        "decision": decision
    }

    response = requests.put(f"http://127.0.0.1:8000/order_confirmation/{customer_number}", json=message_request)
    return response.json()


def send_devis(devis: dict, customer_number):
    response = requests.put(f"http://127.0.0.1:8000/order_devis/{customer_number}", json=devis)
    return response.json()


def send_facture(facture: dict, customer_number):
    response = requests.put(f"http://127.0.0.1:8000/order_facture/{customer_number}", json=facture)
    return response.json()
