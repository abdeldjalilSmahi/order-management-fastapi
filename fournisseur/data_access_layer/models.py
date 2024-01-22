import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase


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


class OrderDalModel(Base):
    __tablename__ = "Orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.customer_id"))
    customer: Mapped[CustomerDalModel] = relationship(back_populates="orders")
