import datetime
import enum
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase


class Status(enum.Enum):
    validee = "Validée"
    annulee = "Annulée"
    initiee = "Initiée"
    en_attente = "En attente"

class Base(DeclarativeBase):
    pass


class CustomerDalModel(Base):
    __tablename__ = "Customers"
    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    orders: Mapped[List["OrderDalModel"]] = relationship(back_populates="customer")

    def __repr__(self):
        data = tuple((self.customer_id, self.firstname,  self.lastname, self.email, self.phone_number))
        return data.__str__()


class OrderDalModel(Base):
    __tablename__ = "Orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.customer_id"))
    customer: Mapped[CustomerDalModel] = relationship(back_populates="orders")


class ProductDalModel(Base):
    __tablename__ = "Products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class HistoriqueDalModel(Base):
    __tablename__ = "Historiques"
    historique_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_historique: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    actual_status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)


