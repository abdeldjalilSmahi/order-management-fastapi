# Models for business logic layer
from datetime import datetime

from fournisseur.data_access_layer.models import CustomerDalModel


class Order:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Product:
    n_article: int
    designation: str
    price: float
    description: str
    quantity: int

    def __init__(self, n_article: int, designation: str, price: float, description: str, quantity: int):
        self.n_article = n_article
        self.designation = designation
        self.price = price
        self.description = description
        self.quantity = quantity


class CustomerBllModel:  # Pour faire les vérification de la commande
    firstname: str
    lastname: str
    email: str
    phone_number: str

    def __init__(self, firstname: str, lastname: str, email: str, phone_number: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number

    @staticmethod
    def is_valid_field(field: str) -> bool:
        return field is not None and field != "string" and field != ""

    def is_valid(self) -> bool:
        return all([
            CustomerBllModel.is_valid_field(self.firstname),
            CustomerBllModel.is_valid_field(self.lastname),
            CustomerBllModel.is_valid_field(self.email)
        ])


class Historique:
    pass


class LigneCommande:
    order: Order
    product: Product
    quantity: int

    def __init__(self, order, product, quantity):
        self.order = order
        self.product = product
        self.quantity = quantity

        # Vous pouvez ajouter ici des validations, par exemple :
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("La quantité doit être un entier positif")

    def calculer_total(self):
        return self.product.price * self.quantity


#
if __name__ == "__main__":
    # Utilisation de la classe
    customer = CustomerBllModel("slahi", "", "john.doe@example.com", "123-456-7890")
    print(customer.__dict__)