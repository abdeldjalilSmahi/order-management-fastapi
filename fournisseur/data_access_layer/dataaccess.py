"""
Data Access Layer pour le client
"""
import business_logic_layer.models
from data_access_layer.database import Database
from business_logic_layer.models import CustomerBllModel, OrderBllModel
from data_access_layer.models import CustomerDalModel
from sqlalchemy import select


class DataAccessCustomer:
    db = Database()

    @staticmethod
    def add_customer(customer: CustomerBllModel):

        with DataAccessCustomer.db.get_session() as session:
            try:
                # Création d'un nouvel objet ClientModel
                nouveau_client = CustomerDalModel(**customer.__dict__)
                # Ajouter le nouvel objet à la session
                session.add(nouveau_client)
                # Valider la transaction
                session.flush()
                session.commit()
                print(f"Le client {nouveau_client.customer_id} a été bien enregistré")
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de l'ajout du client : {e}")
                session.rollback()

    @staticmethod
    def get_all_customers() -> list[CustomerDalModel]:
        with DataAccessCustomer.db.get_session() as session:
            return session.execute(select(CustomerDalModel)).all()

    @staticmethod
    def get_customer_by_id(customer_id: int) -> CustomerDalModel:
        with DataAccessCustomer.db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                print(f"{customer_dal_model}")
                return customer_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du client : {e}")


    @staticmethod
    def get_customer_by_email(email: str) -> CustomerDalModel:
        with DataAccessCustomer.db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.execute(select(CustomerDalModel).filter_by(email=email)).first()
                print(f"{customer_dal_model}")
                return customer_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de la réccupération du client : {e}")




# class DataAccessOrders:
#     db = Database()
#
#     @staticmethod
#     def add_order(order: OrderBllModel):
#         pass
#

if __name__ == "__main__":
    client = business_logic_layer.models.CustomerBllModel(firstname="smahi", lastname="jalil",
                                                                      email="smahi.jilo@gmail.com",
                                                                      phone_number="5848949855")

    # DataAccessClient.get_customer_by_id(2)
    # DataAccessClient.add_customer(client)
    # Example
    # print(DataAccessCustomer.get_customer_by_id(1))

