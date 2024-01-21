"""
Data Access Layer pour le client
"""
import fournisseur.business_logic_layer.models
from fournisseur.data_access_layer.database import Database
from fournisseur.business_logic_layer.models import CustomerBllModel as CustomerBusinessModel
from models import CustomerDalModel


class DataAccessClient:
    @staticmethod
    def ajouter_client(customer: CustomerBusinessModel):
        # Création d'une nouvelle session
        db = Database()
        session = db.get_session()
        try:
            # Création d'un nouvel objet ClientModel
            nouveau_client = CustomerDalModel(firstname=customer.firstname, lastname=customer.lastname
                                              , email=customer.email, phone_number=customer.phone_number)
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


if __name__ == "__main__":
    client = fournisseur.business_logic_layer.models.CustomerBllModel(firstname="smahi", lastname="jalil", email="smahi.jilo@gmail.com",
                                                                      phone_number="5848949855")
    DataAccessClient.ajouter_client(client)
