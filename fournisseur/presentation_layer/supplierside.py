from fastapi import FastAPI, HTTPException, BackgroundTasks, Body, Response, Request
from fastapi.responses import JSONResponse
from business_logic_layer.businessrules import BusinessRulesProducts
from presentation_layer.models import CommandePlModel, Decision
import json
from data_access_layer.constantes import PRODUCTS_LIST
from business_logic_layer.message_queues import envoyer_message_a_queue
app = FastAPI()


@app.get("/products_list")
async def list_products():
    return BusinessRulesProducts.get_all_products()


@app.post("/place_order")
async def place_order(backgroundtasks: BackgroundTasks, commande: CommandePlModel = Body()):
    message = json.dumps(commande.model_dump())
    backgroundtasks.add_task(envoyer_message_a_queue, 'place_order',  message)
    return {"message": "Votre commande a été bien reçu"}

@app.post("/customer_decision/{customer_id}")
async def customer_decision(customer_id: int, backgroundtasks: BackgroundTasks,decision: Decision = Body()):
    data = decision.model_dump()
    data['customer_id'] = customer_id
    message = json.dumps(data)
    print(message)
    backgroundtasks.add_task(envoyer_message_a_queue, 'customer_decision',  message)
    return {"message": "Cher(e) client(e) votre décision a été prise en considération, vous allez recevoir votre "
                       "facture pour faire le paiement"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
