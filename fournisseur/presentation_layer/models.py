import uuid
from pydantic import BaseModel
from typing import Optional, Dict, List


# Base Models : For communication with APIs

class Credentials(BaseModel):
    username: str
    password: str


class CommandePlModel(BaseModel):  #JSON de l'API
    firstname: str
    lastname: str
    email: str
    phone_number: Optional[str] = None
    url: str
    method_name: str
    produits: Dict[str, int]




# Models for Data access layer

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
#
# Base = declarative_base()
#
#
# class Customers(Base):
#     __tablename__ = "customers"
