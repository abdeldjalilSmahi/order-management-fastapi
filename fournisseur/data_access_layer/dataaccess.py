"""
Data Access Layer pour le client
"""
import fournisseur.business_logic_layer.models
from fournisseur.data_access_layer.database import Database
from fournisseur.business_logic_layer.models import CustomerBllModel as CustomerBusinessModel
from models import CustomerDalModel
from sqlalchemy import select


class DataAccessClient:
    db = Database()
    @staticmethod
    def add_customer(customer: CustomerBusinessModel):
        # Création d'une nouvelle session

        session = DataAccessClient.db.get_session()
        try:
            # Création d'un nouvel objet ClientModel
            nouveau_client = CustomerDalModel(**customer.__dict__)
            # Ajouter le nouvel objet à la session
            session.add(nouveau_client)
            # Valider la transaction
            session.commit()
            print(f"Le client {nouveau_client.customer_id} a été bien enregistré")
        except Exception as e:
            # Gérer les exceptions ici
            print(f"Erreur lors de l'ajout du client : {e}")
            session.rollback()
        finally:
            # Fermer la session
            session.close()

    @staticmethod
    def get_customer_by_id(customer_id: int):
        with DataAccessClient.db.get_session() as session:
            try:
                # Creation de la requete
                customer_dal_model = session.query(CustomerDalModel).filter_by(customer_id).scalar_one()
                # nouveau_client = CustomerDalModel(firstname=customer.firstname, lastname=customer.lastname
                #                                   , email=customer.email, phone_number=customer.phone_number)
                # # Ajouter le nouvel objet à la session
                # session.add(nouveau_client)
                # # Valider la transaction
                # session.commit()
                # print(f"Le client {nouveau_client.customer_id} a été bien enregistré")
                print(customer_dal_model)
            except Exception as e:
                # Gérer les exceptions ici
                print(f"Erreur lors de l'ajout du client : {e}")
                session.rollback()


if __name__ == "__main__":
    client = fournisseur.business_logic_layer.models.CustomerBllModel(firstname="smahi", lastname="jalil", email="smahi.jilo@gmail.com",
                                                                      phone_number="5848949855")
    DataAccessClient.add_customer(client)
