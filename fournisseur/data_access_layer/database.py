# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# connection_string = "mssql+pyodbc://jalil:Awtbp!718293@process.database.windows.net:1433/orderManagement?driver=ODBC+Driver+18+for+SQL+Server"
# class Database:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Database, cls).__new__(cls)
#             engine = create_engine(connection_string)
#             Base.metadata.create_all(engine)
#             cls._session_factory = sessionmaker(bind=engine)
#         return cls._instance
#
#     @classmethod
#     def get_session(cls):
#         return cls._session_factory()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base  # Mis à jour pour SQLAlchemy 2.0
import threading
from fournisseur.data_access_layer.models import Base

connection_string = "mssql+pyodbc://jalil:Awtbp!718293@porcess-cloud.database.windows.net:1433/ordermanagement?driver=ODBC+Driver+18+for+SQL+Server&Connection Timeout=3600"


class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, connection_string = "mssql+pyodbc://jalil:Awtbp!718293@porcess-cloud.database.windows.net:1433/ordermanagement?driver=ODBC+Driver+18+for+SQL+Server&Connection Timeout=3600"):
        try:
            self.engine = create_engine(connection_string)
            self.Session = sessionmaker(bind=self.engine)
            self.create_tables()
        except Exception as e:
            pass

    def create_tables(self):

        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()


def test_session_creation():
    session = Database.get_session()
    try:
        result = session.execute(text("SELECT 1"))
        assert result is not None, "La session n'a pas été créée correctement"
    finally:
        session.close()


if __name__ == "__main__":
    # Initialisez la base de données. Cela doit être fait avant d'essayer de créer ou d'interagir avec la base de données
    db = Database(connection_string)
    session = db.get_session()
    try:
        # Exécutez une requête de test
        result = session.execute(text("SELECT 1"))
        print('hi')
        assert result is not None, "La session n'a pas été créée correctement"
    finally:
        session.close()

