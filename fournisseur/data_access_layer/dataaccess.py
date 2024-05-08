"""
Data Access Layer pour le client
"""
import time

from sqlalchemy.orm import Session

import business_logic_layer.models
from data_access_layer.database import Database
from business_logic_layer.models import CustomerBllModel, OrderBllModel, ProductBllModel
from data_access_layer.models import CustomerDalModel, OrderDalModel, ProductDalModel, OrderLinesDalModel, Status, \
    HistoriqueDalModel, Events
from sqlalchemy import select, desc

"""
Gérer les transaction efficacement
"""


class DataAccessorTransaction:
    ### Customer ###
    """
    Methodes pour manipuler les transactions sur customers
    """

    @staticmethod
    def add_customer(customer_bll_model: CustomerBllModel) -> CustomerDalModel:
        db = Database()
        try:
            with db.get_session() as session:
                email = customer_bll_model.email
                customer_dal_model = session.query(CustomerDalModel).filter_by(email=email).first()

                if customer_dal_model is None:
                    # Création d'un nouvel objet ClientModel
                    customer_data = customer_bll_model.__dict__.copy()
                    customer_data.pop('customer_id', None)  # Supprimer 'customer_id' si présent
                    customer_dal_model = CustomerDalModel(**customer_data)
                    # Ajouter le nouvel objet à la session
                    session.add(customer_dal_model)
                    # La session est automatiquement commitée à la fin du bloc with
                    session.commit()
                    session.refresh(customer_dal_model)
                    print(f"Le client {customer_dal_model.customer_id} a été bien enregistré")
                    return customer_dal_model
                else:
                    print(f"Le client dont l'email {email} existe déjà.")
                    return customer_dal_model
        except Exception as e:
            print(f"Erreur lors de l'ajout du client : {e}")
            raise  # Relancer l'exception pour la gestion d'erreur à un niveau supérieur.

    @staticmethod
    def get_all_customers() -> list[CustomerDalModel]:
        db = Database()
        with db.get_session() as session:
            return session.scalars(select(CustomerDalModel).order_by(CustomerDalModel.customer_id)).all()

    @staticmethod
    def get_customer_by_id(customer_id: int) -> CustomerDalModel:
        db = Database()
        with db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                return customer_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du client : {e}")

    @staticmethod
    def get_customer_by_email(email: str) -> CustomerDalModel:
        db = Database()
        with db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.execute(select(CustomerDalModel).filter_by(email=email)).first()
                print(f"{customer_dal_model}")
                return customer_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du client : {e}")

    @staticmethod
    def delete_customer(customer_id: int):
        db = Database()
        with db.get_session() as session:
            try:
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                session.delete(customer_dal_model)
                session.commit()
                session.refresh(customer_dal_model)
                print(f"Customer {customer_id} was successfully deleted")
            except Exception as e:
                print(f"Erreur lors de la suppression du client : {e}")
                session.rollback()

    @staticmethod
    def update_customer(customer_id: int, customer: CustomerBllModel):
        db = Database()
        with db.get_session() as session:
            try:
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                if customer_dal_model is None:
                    print("Customer not found")
                    return
                    # Création d'un nouvel objet ClientModel
                customer_data = customer.__dict__.copy()
                customer_data.pop('customer_id', None)  # Supprimer 'customer_id' si présent
                for key, value in customer_data.items():
                    if hasattr(customer_dal_model, key):
                        setattr(customer_dal_model, key, value)
                session.commit()
                session.refresh(customer_dal_model)
                print(f"Customer {customer_id} was successfully updated")
            except Exception as e:
                print(f"Error updating customer: {e}")
                session.rollback()

    ### Fin Customer ###
    ### Order #####
    """
    Methodes pour manipuler les transactions sur orders
    """

    @staticmethod
    def add_order(customer_id: int, order_number:int) -> OrderDalModel:
        db = Database()
        with db.get_session() as session:
            try:
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                if customer_dal_model is None:
                    print("Customer does not exist")
                    return
                new_order = OrderDalModel(customer_id=customer_dal_model.customer_id, order_number= order_number)
                session.add(new_order)  ## Est ce que je mets session.add ou non
                customer_dal_model.orders.append(new_order)
                new_order.customer = customer_dal_model
                ###
                historique = HistoriqueDalModel(order_id=new_order.order_id)
                session.add(historique)
                historique.order = new_order
                new_order.historiques.append(historique)

                session.commit()
                print(f"Order {new_order.order_id} was successfully added")
                return new_order
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de l'ajout de la commande : {e}")
                session.rollback()

    @staticmethod
    def get_order_by_id(order_id):
        db = Database()
        with db.get_session() as session:
            try:
                # Creation de la requete
                order_dal_model = session.get(OrderDalModel, order_id)
                return order_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du client : {e}")

    @staticmethod
    def update_order_status(order_id: int, status: Status) -> OrderDalModel:
        db = Database()
        with db.get_session() as session:
            try:
                order_dal_model = session.get(OrderDalModel, order_id)
                if order_dal_model is None:
                    print("Order does not exist")
                    return
                order_dal_model.actual_status = status
                historique_dal_model = HistoriqueDalModel(order_id=order_id, event=Events.updated, actual_status=status)
                session.add(historique_dal_model)
                historique_dal_model.order = order_dal_model
                order_dal_model.historiques.append(historique_dal_model)
                session.add(order_dal_model)
                session.refresh(order_dal_model)
                session.refresh(historique_dal_model)
                session.commit()
                session.refresh(order_dal_model)
                session.refresh(historique_dal_model)
                return order_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la modification du status de la commande : {e}")
                session.rollback()

    @staticmethod
    def get_order_status(order_id: int):
        db = Database()
        with db.get_session() as session:
            try:
                order_dal_model = session.get(OrderDalModel, order_id)
                if order_dal_model is None:
                    print("Order does not exist")
                    return
                return order_dal_model.actual_status
            except Exception as e:
                print(f"Une exception {e} est levé lors de la reccuperation du order")

    @staticmethod
    def cancel_order(order_id: int):
        db = Database()
        with db.get_session() as session:
            try:
                order_dal_model = session.get(OrderDalModel, order_id)

                if order_dal_model is None:
                    print("Order does not exist")
                    return
                cancel_cases = [
                    Status.cancelled_by_customer,
                    Status.cancelled_by_seller,
                    Status.payment_failed,
                    Status.returned,
                    Status.refunded,
                    Status.cancelled_and_finished
                ]
                if order_dal_model.actual_status == Status.cancelled_and_finished:
                    print("Cette commande a été deja cloturé et on a rendu le stock a son état d'avant")
                    return
                else:

                    order_lines = session.query(OrderLinesDalModel).filter_by(order_id=order_dal_model.order_id).all()
                    for order_line in order_lines:
                        product_id = order_line.product_id
                        product = session.get(ProductDalModel, product_id)
                        session.add(product)
                        product.quantity += order_line.quantity_ordered
                    status = Status.cancelled_and_finished
                    order_dal_model.actual_status = status
                    historique_dal_model = HistoriqueDalModel(order_id=order_id, event=Events.updated
                                                              , actual_status=status)
                    session.add(historique_dal_model)
                    order_dal_model.historiques.append(historique_dal_model)
                    session.add(order_dal_model)
                    session.commit()
                    session.refresh(order_dal_model)
                    session.refresh(historique_dal_model)

            except Exception as e:
                print(f"{e}")

    @staticmethod
    def get_last_order_initie_of_customer(customer_id: int):
        db = Database()
        with db.get_session() as session:
            try:
                last_order = session.query(OrderDalModel) \
                    .filter_by(customer_id=customer_id, actual_status=Status.initiated) \
                    .order_by(desc(OrderDalModel.order_date)) \
                    .first()

                if last_order is not None:
                    print(f"Order {last_order.order_id} was successfully founded")
                    return last_order
                else:
                    print("Aucune commande initiee trouvee pour ce client.")
                    return None

            except Exception as e:
                print(f"Erreur lors de la recherche de la commande : {e}")
                return None

    ###Products ####
    """
    Products
    """

    @staticmethod
    def add_product(product: ProductBllModel):
        db = Database()
        with db.get_session() as session:
            try:
                # Création d'un nouvel objet ClientModel
                new_product = ProductDalModel(**product.__dict__)
                # Ajouter le nouvel objet à la session
                session.add(new_product)
                # Valider la transaction

                session.commit()
                session.refresh(new_product)
                print(f"Le produit {new_product.product_id} a été bien enregistré")
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de l'ajout du client : {e}")
                session.rollback()

    @staticmethod
    def get_all_products() -> list[ProductDalModel]:
        db = Database()
        with db.get_session() as session:
            return session.scalars(select(ProductDalModel).order_by(ProductDalModel.product_id)).all()

    @staticmethod
    def get_all_products_details() -> list[tuple]:
        db = Database()
        with db.get_session() as session:
            # Construire la requête pour sélectionner les colonnes désirées
            query = select(ProductDalModel.product_name, ProductDalModel.unit_price).order_by(
                ProductDalModel.product_id)
            # Exécuter la requête et récupérer les résultats sous forme de liste de tuples
            result = session.execute(query).fetchall()
            return result

    @staticmethod
    def get_all_products_name() -> list[str]:
        db = Database()
        with db.get_session() as session:
            return session.scalars(select(ProductDalModel.product_name).order_by(ProductDalModel.product_id)).all()

    @staticmethod
    def get_product_by_name(product_name: str) -> ProductDalModel:
        db = Database()
        with db.get_session() as session:
            try:
                # Creation de la requete
                product_dal_model = session.query(ProductDalModel).filter_by(product_name=product_name).first()
                return product_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du product : {e}")

    @staticmethod
    def update_product_quantity(product_id, quantity: int) -> None:
        db = Database()
        try:
            with db.get_session() as session:
                product = session.get(ProductDalModel, product_id)
                if product is None:
                    print("Product does not exsist")
                    return
                if quantity < 0:
                    print("Quantity negative")
                    return
                product.quantity = quantity
                session.commit()
                session.refresh(product)
        except Exception as e:
            print(f"Error updating product: {e}")
            session.rollback()

    ### FIN Product####
    """
    Order Lines
    """

    @staticmethod
    def add_order_line(order_id: int, product_id: int, quantity_ordered: int):
        db = Database()
        with db.get_session() as session:
            try:
                # Vérifiez si la commande et le produit existent
                order_dal_model = session.get(OrderDalModel, order_id)
                product_dal_model = session.get(ProductDalModel, product_id)

                if order_dal_model is None or product_dal_model is None:
                    print("Order or Product does not exist")
                    return
                if quantity_ordered < 0:
                    print("Quantity negative")
                    return
                remain_quantity = product_dal_model.quantity - quantity_ordered

                if remain_quantity < 0:
                    print("Quantity negative")
                    return

                # Créez une nouvelle ligne de commande
                new_order_line = OrderLinesDalModel(
                    order_id=order_id,
                    product_id=product_id,
                    quantity_ordered=quantity_ordered
                )

                # Ajoutez la nouvelle ligne de commande à la session et enregistrez-la dans la base de données
                session.add(new_order_line)
                product_dal_model.quantity = remain_quantity
                order_dal_model.products.append(new_order_line)
                product_dal_model.orders.append(new_order_line)
                new_order_line.order = order_dal_model
                new_order_line.product = product_dal_model
                session.commit()
                session.refresh(new_order_line)
                session.refresh(product_dal_model)
                session.refresh(order_dal_model)
                print(f"Order line for order {order_id} and product {product_id} was successfully added")
            except Exception as e:
                print(f"Erreur lors de l'ajout de la ligne de commande : {e}")
                session.rollback()
