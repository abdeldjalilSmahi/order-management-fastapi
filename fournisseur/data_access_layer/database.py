from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base  # Mis à jour pour SQLAlchemy 2.0
import threading

import data_access_layer.models
from data_access_layer.models import Base
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",  # Dialecte et driver pour MySQL
    username="jalil",
    password="Awtbp!718293",  # Remplacez par votre mot de passe réel
    host="processus.mysql.database.azure.com",
    port=3306,
    database="ordermanagement",  # Remplacez par le nom de votre base de données
    query={
        "ssl_disabled": "False"
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
            self.session = Session(bind=self.engine, autoflush=True)
            self.create_tables()
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {e}")

    def create_tables(self):

        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.session


if __name__ == "__main__":
    # Initialisez la base de données. Cela doit être fait avant d'essayer de créer ou d'interagir avec la base de données
    db = Database()
    session = db.get_session()
    try:
        # Exécutez une requête de test
        data = session.query(data_access_layer.models.CustomerDalModel.firstname).all()

        for row in data:
            print(row)
    finally:
        session.close()
