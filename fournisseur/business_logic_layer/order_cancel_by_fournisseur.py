"""
Ce fichier, définit le processus d'annulation d'une commande par le fournisseur.
"""
from data_access_layer.models import Status
from data_access_layer.dataaccess import DataAccessOrders


def order_cancel_by_fournisseur(order_id: int, status: Status):
    pass
