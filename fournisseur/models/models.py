from pydantic import BaseModel
import uuid


class Commande(BaseModel):
    id_commande: str = str(uuid.uuid4())
    description: str


class CommandeModel(BaseModel):
    description : str

#
# commande = Commande(description="Votre description ici")
# commande_model = CommandeModel(commande=commande)
# commande = Commande(**commande_model.commande.__dict__)
# print(commande.__dict__)

commandeModel = CommandeModel(description="la description de oussama ")
data = commandeModel.__dict__
description = data["description"]
cmd = Commande(description=description)
print(cmd.id_commande)