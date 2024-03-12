# order-management-fastapi

## Installation
Afin d'utiliser ce repot, nous vous invitons de créer tout d'abord un environnement virtuel:

Création de l'environnement virtuel: __python -m venv venv__

Activation:
-  __Windows:__ .\venv\Scrpits\activate.bat
- __linux:__ : source venv\bin\activate



Puis installez les requirements (les librairies pour tourner le projet): 

__pip install -r requirements.txt__


puis executez :
-  cd .\fournisseur
-  **pip install -e .**


## Execution
### Lancez le serveur uvicorn
Assurez vous que vous etes dans le répertoire : order-management-fastapi et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** python fournisseur\presentation_layer\supplierside.py

### Lancement des workers (order verification)
À partir d'un autre cmd (ou d'autres CMD autant de CMD que worker) :

Assurez vous que vous etes dans le répertoire : order-management-fastapi et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** python fournisseur\business_logic_layer\order_verification.py


### Lancement des workers (inventory checking)

À partir d'un autre cmd (ou d'autres CMD autant de CMD que worker) :

Assurez vous que vous etes dans le répertoire : order-management-fastapi et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** python fournisseur\business_logic_layer\inventory_checking.py

### Lancement des workers (devis generation)

À partir d'un autre cmd (ou d'autres CMD autant de CMD que worker) :

Assurez vous que vous etes dans le répertoire : order-management-fastapi et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** python fournisseur\business_logic_layer\devis_generation.py

### Lancement des workers (customer decision)

À partir d'un autre cmd (ou d'autres CMD autant de CMD que worker) :

Assurez vous que vous etes dans le répertoire : order-management-fastapi et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** python fournisseur\business_logic_layer\customer_decision.py

### Lancement du dashboard

À partir d'un autre cmd :

Assurez-vous que cette fois-ci vous êtes dans le répertoire : **order-management-fastapi/DashBoard** et que vous avez bien créé un venv et installé les requirements.

**Exectuez:** streamlit run  DashBoard\streamlite.py


