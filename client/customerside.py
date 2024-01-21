import requests

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8000"  # Remplacez par l'URL de votre API

# Données de l'utilisateur pour la session
user_data = {
    "username": "user1",
    "password": "password1"
}

# Ouvrir une session
session_response = requests.post(f"{BASE_URL}/open_session", json=user_data)
print(session_response.json())

if session_response.status_code == 200:
    print("Session ouverte avec succès")
    # Récupérer les cookies de session
    cookies = session_response.cookies

    # Données de la commande
    commande_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        # "email": "email facultatif" # Si vous voulez inclure un email
    }

    # Passer une commande
    order_response = requests.post(f"{BASE_URL}/place_order", json=commande_data, cookies=cookies)

    if order_response.status_code == 200:
        print("Commande passée avec succès :", order_response.json())
    else:
        print("Erreur lors de la commande :", order_response.text)
else:
    print("Erreur lors de l'ouverture de session :", session_response.text)
