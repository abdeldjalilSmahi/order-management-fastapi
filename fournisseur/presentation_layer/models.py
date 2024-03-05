import uuid
from pydantic import BaseModel
from typing import Optional, Dict, List


# Base Models : For communication with APIs

class Credentials(BaseModel):
    username: str
    password: str


class CommandePlModel(BaseModel):  #JSON de l'API
    customer_number : str
    firstname: str
    lastname: str
    email: str
    phone_number: Optional[str] = None
    order_number: int
    # url: str
    # method_name: str
    produits: Dict[str, int]

class Decision(BaseModel):
    customer_number: str
    order_id : int
    order_number : int
    status : str



# Models for Data access layer

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
#
# Base = declarative_base()
#
#
# class Customers(Base):
#     __tablename__ = "customers"
