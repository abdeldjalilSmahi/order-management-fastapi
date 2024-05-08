from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base  # Mis à jour pour SQLAlchemy 2.0
import threading

import data_access_layer.models
from data_access_layer.models import Base
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",
    username="*****",
    password="*****",
    host="processus.mysql.database.azure.com",
    port=3306,
    database="ordermanagement",
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


