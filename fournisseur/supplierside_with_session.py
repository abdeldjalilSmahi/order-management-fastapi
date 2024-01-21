from fastapi import FastAPI, HTTPException, BackgroundTasks, Body, Response, Request
from fastapi.responses import JSONResponse
from presentation_layer.models import CommandePlModel, Commande, Credentials
import pika
import json
import secrets

app = FastAPI()



fake_db = {"user1": "password1"}


@app.post("/open_session")
async def open_session(credentials: Credentials, response: Response):
    # Vérifier les identifiants (à remplacer par une vraie validation)
    if fake_db.get(credentials.username) == credentials.password:
        session_token = secrets.token_urlsafe()
        response.set_cookie(key="session_token", value=session_token)
        return {"message": "Session ouverte"}
    raise HTTPException(status_code=401, detail="Identifiants incorrects")


# @app.get("/get_products")
# async def get_products():
#     return products


# Fonction pour vérifier la session
def verify_session(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        return True
    return False


@app.post("/place_order")
async def place_order(request: Request, backgroundtasks: BackgroundTasks, commande: CommandePlModel = Body()):
    if not verify_session(request):
        raise HTTPException(status_code=401, detail="Session non valide ou expirée")

    message = "test"
    backgroundtasks.add_task(envoyer_message_a_queue, message)
    return {"message": "Votre commande a été bien reçu"}


def envoyer_message_a_queue(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ma_queue')
    channel.basic_publish(exchange='', routing_key='ma_queue', body=message)
    channel.close()
    connection.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
