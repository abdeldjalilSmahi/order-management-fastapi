# Models for business logic layer
import datetime
import enum
from typing import Optional
from data_access_layer.models import Status, Events


# class Status(enum.Enum):
#     validee = "Validée"
#     annulee = "Annulée"
#     initiee = "Initiée"
#     en_attente = "En attente"
#
#
# class Events(enum.Enum):
#     create = "Create"
#     update = "Update"
#     delete = "Delete"


class CustomerBllModel:  # Pour faire les vérification de la commande
    customer_id = Optional[int]
    customer_number: str
    firstname: str
    lastname: str
    email: str
    phone_number: str

    def __init__(self, customer_number: str, firstname: str, lastname: str, email: str, phone_number: str,
                 customer_id: Optional[int] = None):
        self.customer_id = customer_id
        self.customer_number = customer_number
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number


class OrderBllModel:
    order_id: int
    order_number: int
    order_date: datetime.datetime
    customer_id: int
    actual_status: Status
    customer: CustomerBllModel

    def __init__(self, order_id: int, order_number,  order_date: datetime.datetime, customer_id: int, actual_status: Status,
                 customer: CustomerBllModel):
        self.order_id = order_id
        self.order_number = order_number
        self.order_date = order_date
        self.customer_id = customer_id
        self.actual_status = actual_status
        self.customer = customer

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "order_number": self.order_number,
            "order_date": self.order_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "customer_id": self.customer_id,
            "actual_status": self.actual_status.value
        }


class ProductBllModel:
    product_id = Optional[int]
    product_name: str
    unit_price: float
    description: str
    quantity: int

    def __init__(self, product_name: str, unit_price: float, description: str, quantity: int,
                 product_id: Optional[int] = None):
        self.product_id = product_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.description = description
        self.quantity = quantity


class Historique:
    pass


# class LigneCommande:
#     order: Order
#     product: Product
#     quantity: int
#
#     def __init__(self, order, product, quantity):
#         self.order = order
#         self.product = product
#         self.quantity = quantity
#
#         # Vous pouvez ajouter ici des validations, par exemple :
#         if not isinstance(quantity, int) or quantity < 1:
#             raise ValueError("La quantité doit être un entier positif")
#
#     def calculer_total(self):
#         return self.product.price * self.quantity


#
if __name__ == "__main__":
    # Utilisation de la classe
    customer = CustomerBllModel("slahi", "", "john.doe@example.com", "123-456-7890")
    print(customer.__dict__)
