from datetime import datetime

from business_logic_layer.models import CustomerBllModel, ProductBllModel, OrderBllModel
import validators
import re

from validators.utils import ValidationError

from data_access_layer.dataaccess import DataAccessProduct, DataAccessorTransaction
from data_access_layer.database import Database
from data_access_layer.models import Status


class BusinessRulesCustomer:
    @staticmethod
    def verify_business_rules(customer_bll_model: CustomerBllModel):
        if not customer_bll_model.firstname or customer_bll_model.firstname.lower() == "string":
            return False
        if not customer_bll_model.lastname or customer_bll_model.lastname.lower() == "string":
            return False
        if not validators.email(customer_bll_model.email):
            return False
        if not BusinessRulesCustomer.is_valid_phone_number(customer_bll_model.phone_number):
            return False
        return True

    @staticmethod
    def is_valid_phone_number(phone_number: str) -> bool:
        if phone_number is None or phone_number.lower() == "string":
            return False

        # Expression régulière pour valider les formats de numéro de téléphone
        # Accepte les formats comme "0764177198" ou "+33764177198"
        phone_pattern = r'^(?:\+\d{2})?\d{10}$'

        return re.match(phone_pattern, phone_number) is not None

    @staticmethod
    def add_customer(customer_bll_model: CustomerBllModel):
        try:
            customer_dal_model = DataAccessorTransaction.add_customer(customer_bll_model)
            return customer_dal_model.to_dict()
        except Exception as e:
            print(f"erreur lors de l'ajout du customer.")


    @staticmethod
    def get_customer_by_id(customer_id : int):
        try:
            return CustomerBllModel(**DataAccessorTransaction.get_customer_by_id(customer_id).to_dict())
        except Exception as e:
            print(f"erreur lors de la réccupération du customer.")


class BusinessRulesProducts:
    @classmethod
    def get_all_products(cls):
        product_names_in_database = set(DataAccessorTransaction.get_all_products_details())
        dictionnaire = {}
        for each_tuple in product_names_in_database:
            dictionnaire[each_tuple[0]] = each_tuple[1]
        return dictionnaire

    @classmethod
    def _verify_products_names(cls, product_names_bll_model: list[str]):
        for product_name_bll_model in product_names_bll_model:
            if not product_name_bll_model or product_name_bll_model.lower() == "string":
                return False

        product_names_in_database = set(DataAccessorTransaction.get_all_products_name())
        for product_name_bll_model in product_names_bll_model:
            if product_name_bll_model not in product_names_in_database:
                return False

        return True

    @staticmethod
    def verify_products_names_and_positive_quantities(products_with_quantities: dict[str, int]):
        if not products_with_quantities:
            return False
        keys = list(products_with_quantities.keys())
        verification = BusinessRulesProducts()._verify_products_names(keys)
        if not verification:
            return False

        for quantity in products_with_quantities.values():
            if quantity <= 0:
                return False

        return True

    @staticmethod
    def verify_inventory_quantities(products_with_quantities: dict[str, int]):

        keys = list(products_with_quantities.keys())
        verification = BusinessRulesProducts()._verify_products_names(keys)
        if not verification:
            return False
        for key, quantity in products_with_quantities.items():
            product_dal_model = DataAccessorTransaction.get_product_by_name(key)
            if product_dal_model.quantity <= 0:
                motif = "Quantité insuffisante dans le stock"
                return False, motif

            if quantity > product_dal_model.quantity:
                motif = "Quantité demandée est supperieure de celle dans le stock"
                return False, motif
            motif = "Quantité suffisante !"
            return True, motif

    @staticmethod
    def get_product_by_name(product_name: str):
        product_bll_model = ProductBllModel(**DataAccessorTransaction.get_product_by_name(product_name).to_dict())
        return product_bll_model


class BusinessRulesOrder:
    def __init__(self, customer: CustomerBllModel, order: OrderBllModel, order_lines: dict[str, int]):
        self.customer = customer
        self.order = order
        self.order_lines = order_lines

    def update_order_status(self, status: Status):
        try:
            self.order.status = status
            DataAccessorTransaction.update_order_status(self.order.order_id, self.order.status)
        except Exception as e:
            print(f"Erreur lors de la modification du status de l'order : {e}")
        return self.order.status

    def cancel_order(self):
        try:
            order_id = self.order.order_id
            DataAccessorTransaction.cancel_order(order_id)
        except Exception as e:
            print("Erreur lors de la suppression des lignes de commandes ")

    @staticmethod
    def termine_order(order):
        try:
            order_id = order.order_id
            DataAccessorTransaction.cancel_order(order_id)
        except Exception as e:
            print("Erreur lors de la suppression des lignes de commandes ")

    @staticmethod
    def add_order(customer: CustomerBllModel, order_number: int) -> OrderBllModel:
        try:
            order_dal_model = DataAccessorTransaction.add_order(customer_id=customer.customer_id,
                                                                order_number=order_number)
            return OrderBllModel(customer=customer, **order_dal_model.to_dict())
        except Exception as e:
            print("Erreur lors de l'ajout de la commande")

    @staticmethod
    def get_last_order_initie_of_customer(customer: CustomerBllModel) -> OrderBllModel:
        try:
            order_dal_model = DataAccessorTransaction.get_last_order_initie_of_customer(customer.customer_id)
            order_bll_model = OrderBllModel(customer=customer, **order_dal_model.to_dict())
            return order_bll_model
        except Exception as e:
            pass

    @staticmethod
    def update_status_order(order_bll_model: OrderBllModel, status: Status):
        try:
            DataAccessorTransaction.update_order_status(order_bll_model.order_id, status)
            order_bll_model.actual_status = status
        except Exception as e:
            print(f"Erreur lors de la modification du status de l'order : {e}")
        return order_bll_model

    @staticmethod
    def get_order_by_id(customer: CustomerBllModel, order_id: int) -> OrderBllModel:
        try:
            order_dal_model = DataAccessorTransaction.get_order_by_id(order_id)
            order_bll_Model = OrderBllModel(customer=customer, **order_dal_model.to_dict())
            return order_bll_Model
        except Exception as e:
            print("Errer lors de la réccupération de l'order : " + str(e))

    @staticmethod
    def construct_order_bll_model_factory(customer_bll_model, order_bll_model, order_lines):
        order_bll_model["actual_status"] = Status.get_status_by_name(order_bll_model["actual_status"])
        order_bll_model["order_date"] = datetime.strptime(order_bll_model["order_date"], "%Y-%m-%dT%H:%M:%S")
        order_bll_model["customer"] = customer_bll_model
        order_bll_model = OrderBllModel(**order_bll_model)
        return BusinessRulesOrder(customer_bll_model, order_bll_model, order_lines)

    def to_dict(self):
        return {
            "customer": self.customer.__dict__,
            "order": self.order.to_dict(),
            "order_lines": self.order_lines
        }


class BusinessRulesOrderLines:
    def __init__(self, order_bll_model: OrderBllModel, product_bll_model: ProductBllModel, quantity):
        self.order_bll_model = order_bll_model
        self.product_bll_model = product_bll_model
        self.quantity = quantity

    @classmethod
    def add_order_line(cls, order_bll_model, product_bll_model, quantity):
        try:
            DataAccessorTransaction.add_order_line(order_bll_model.order_id, product_bll_model.product_id, quantity)
            print("Order line was successfully added")
        except Exception as e:
            print(f"Exception et rollback {e}")


if __name__ == '__main__':
    # customer = CustomerBllModel("smahi", "jalil", "smahi.jilo@gmail.com", "0764177193")
    products = {
        "prouct1": 5,
        "prouct2": 10
    }
    print(BusinessRulesProducts.verify_products_names_and_positive_quantities(products))
