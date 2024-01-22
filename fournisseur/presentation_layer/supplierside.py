from fastapi import FastAPI, HTTPException, BackgroundTasks, Body, Response, Request
from fastapi.responses import JSONResponse
from fournisseur.presentation_layer.models import CommandePlModel
import json
from fournisseur.data_access_layer.constantes import PRODUCTS_LIST
from fournisseur.business_logic_layer.message_queues import envoyer_message_a_queue
app = FastAPI()


@app.get("/products_list")
async def list_products():
    return PRODUCTS_LIST


@app.post("/place_order")
async def place_order(backgroundtasks: BackgroundTasks, commande: CommandePlModel = Body()):
    message = json.dumps(commande.model_dump())
    backgroundtasks.add_task(envoyer_message_a_queue,'place_order',  message)
    return {"message": "Votre commande a été bien reçu"}


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8000)
