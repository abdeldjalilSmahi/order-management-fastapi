# test.py
from sqlalchemy import create_engine, exc
from sqlalchemy.sql import text

from data_access_layer.models import Status


# Tester la connexion à la base de données  !
# REUSSI :D
def test_connection():
    connection_string = "mssql+pyodbc://jalil:Awtbp!718293@process.database.windows.net:1433/orderManagement?driver=ODBC+Driver+18+for+SQL+Server"

    try:
        # Création de l'engine
        engine = create_engine(connection_string)
        # Exécution d'une requête simple pour tester la connexion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            for row in result:
                print("Connexion réussie, résultat :", row[0])
    except exc.SQLAlchemyError as e:
        print("Erreur lors de la connexion à la base de données :", e)


if __name__ == "__main__":
    string_value = "On Hold"


    print(corresponding_status)
