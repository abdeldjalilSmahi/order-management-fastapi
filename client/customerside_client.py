import requests


def passer_commande(request_message: dict):
    response = requests.post("http://127.0.0.1:8000/place_order", json=request_message)
    return response.json()


if __name__ == '__main__':
    URL_POST_ANSWER = "127.0.0.1:8080/get-answer"
    METHOD_NAME = "POST"
    FIRSTNAME = "Jalil"
    LASTNAME = "SMAHI"
    EMAIL = "smahi.jilo@gmail.com"
    PRODUCTS = {"produit1": 2, "produit2": 3}
    request_message = {"firstname": FIRSTNAME, "lastname": LASTNAME, "email": EMAIL, "url": URL_POST_ANSWER,
                       "method_name": METHOD_NAME, "produits": PRODUCTS}

    print(passer_commande(request_message))
