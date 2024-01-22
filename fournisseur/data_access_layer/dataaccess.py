"""
Data Access Layer pour le client
"""
import fournisseur.business_logic_layer.models
from fournisseur.data_access_layer.database import Database
from fournisseur.business_logic_layer.models import CustomerBllModel, OrderBllModel
from models import CustomerDalModel, OrderDalModel
from sqlalchemy import select


class DataAccessClient:
    db = Database()

    @staticmethod
    def add_customer(customer: CustomerBllModel):

        with DataAccessClient.db.get_session() as session:
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
    def get_customer_by_id(customer_id: int) -> CustomerDalModel:
        with DataAccessClient.db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.get(CustomerDalModel, customer_id)
                print(f"{customer_dal_model}")
                return customer_dal_model
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de l'ajout du client : {e}")


class DataAccessOrders:
    db = Database()

    @staticmethod
    def add_order(order: OrderBllModel):
        pass


if __name__ == "__main__":
    client = fournisseur.business_logic_layer.models.CustomerBllModel(firstname="smahi", lastname="jalil",
                                                                      email="smahi.jilo@gmail.com",
                                                                      phone_number="5848949855")
    db = Database()
    # Example
    with db.get_session() as session:
        print(type(session.scalars(select(CustomerDalModel.customer_id).order_by(CustomerDalModel.customer_id)).all()))
