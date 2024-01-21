from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

Base = declarative_base()


class CustomerDalModel(Base):
    __tablename__ = "Customers"
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=True)



# class Order(Base):
#     __tablename__ = "Orders"
#     order_id = Column(Integer, primary_key=True, autoincrement=True)
#     order_date = Column(String(50), nullable=False)
