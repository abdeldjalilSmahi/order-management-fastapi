

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base  # Mis à jour pour SQLAlchemy 2.0
import threading

import fournisseur.data_access_layer.models
from fournisseur.data_access_layer.models import Base
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mssql+pyodbc",
    username="jalil",
    password="Awtbp!718293",  # Remplacez par votre mot de passe réel
    host="porcess-cloud.database.windows.net",
    port=1433,
    database="ordermanagement",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "yes",
        "Connection Timeout": "0"
    }
)



class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self,
                    connection_string=connection_url):
        try:
            self.engine = create_engine(connection_string)
            self.session = Session(bind=self.engine)
            self.create_tables()
        except Exception as e:
            pass

    def create_tables(self):

        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.session


def test_session_creation():
    session = Database.get_session()
    try:
        result = session.execute(text("SELECT 1"))
        assert result is not None, "La session n'a pas été créée correctement"
    finally:
        session.close()


if __name__ == "__main__":
    # Initialisez la base de données. Cela doit être fait avant d'essayer de créer ou d'interagir avec la base de données
    db = Database(connection_url)
    session = db.get_session()
    try:
        # Exécutez une requête de test
        data = session.query(fournisseur.data_access_layer.models.CustomerDalModel.firstname).all()

        for row in data:
            print(row)
    finally:
        session.close()
