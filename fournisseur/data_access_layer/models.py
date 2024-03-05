import datetime
import enum
from typing import List, Optional
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Enum, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func


class Status(enum.Enum):
    confiremd_by_customer = "Confirmed by customer"
    validated = "Validated"
    cancelled_by_customer = "Cancelled by Customer"
    initiated = "Initiated"
    pending = "Pending"
    processing = "Processing"
    shipped = "Shipped"
    out_for_delivery = "Out for Delivery"
    delivered = "Delivered"
    returned = "Returned"
    refunded = "Refunded"
    awaiting_payment = "Awaiting Payment"
    payment_failed = "Payment Failed"
    awaiting_confirmation = "Awaiting Confirmation"
    awaiting_stock = "Awaiting Stock"
    cancelled_by_seller = "Cancelled by Seller"
    on_hold = "On Hold"
    cancelled_and_finished = "Cancelled & Finished By Customer/Seller"

    @staticmethod
    def get_status_by_name(string_value: str) -> 'Status':
        for status in Status:
            if status.value == string_value:
                return status
        return None  # ou lever une exception si préféré


class Events(enum.Enum):
    created = "Created"
    updated = "Updated"
    deleted = "Deleted"


class Base(DeclarativeBase):
    pass


class CustomerDalModel(Base):
    __tablename__ = "Customers"
    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_number: Mapped[str] = mapped_column(String(36), unique=True,  nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    orders: Mapped[List["OrderDalModel"]] = relationship(back_populates="customer", cascade="all, delete",
                                                         passive_deletes=True)

    def __repr__(self):
        data = tuple((self.customer_id, self.customer_number, self.firstname, self.lastname, self.email
                      , self.phone_number))
        return data.__str__()

    def to_dict(self) -> dict:
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phone_number": self.phone_number,
            "customer_number": self.customer_number,
            "customer_id": self.customer_id
        }


class OrderDalModel(Base):
    __tablename__ = "Orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    order_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customers.customer_id", ondelete="CASCADE"))
    actual_status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.initiated)
    customer: Mapped[CustomerDalModel] = relationship(back_populates="orders")
    products = relationship("OrderLinesDalModel", back_populates="order")
    historiques: Mapped[List["HistoriqueDalModel"]] = relationship(back_populates="order")

    def __repr__(self):
        data = tuple((self.order_id,  self.order_number, self.order_date, self.customer_id, self.actual_status.name))
        return data.__str__()

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "order_number": self.order_number,
            "order_date": self.order_date,
            "customer_id": self.customer_id,
            "actual_status": self.actual_status
        }


class ProductDalModel(Base):
    __tablename__ = "Products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint('quantity>=0'), nullable=False, default=0)
    orders: Mapped[List["OrderLinesDalModel"]] = relationship(back_populates="product")

    def __repr__(self):
        data = tuple((self.product_id, self.product_name, self.unit_price, self.description, self.quantity))
        return data.__str__()

    def to_dict(self) ->dict:
        return{
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit_price": self.unit_price,
            "description": self.description,
            "quantity": self.quantity,
        }


class HistoriqueDalModel(Base):
    __tablename__ = "Historiques"
    historique_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("Orders.order_id", ondelete="CASCADE"), nullable=False)
    date_historique: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    event: Mapped[Events] = mapped_column(Enum(Events), default=Events.created, nullable=False)
    actual_status: Mapped[Status] = mapped_column(Enum(Status), default=Status.initiated, nullable=False)
    order: Mapped[OrderDalModel] = relationship(back_populates="historiques")


class OrderLinesDalModel(Base):
    __tablename__ = "OrderLines"
    order_id: Mapped[int] = mapped_column(ForeignKey("Orders.order_id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("Products.product_id"), primary_key=True)
    quantity_ordered: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity_ordered>0"), nullable=False)
    product: Mapped["ProductDalModel"] = relationship("ProductDalModel", back_populates="orders")
    order: Mapped["OrderDalModel"] = relationship("OrderDalModel", back_populates="products")


if __name__ == "__main__":
    pass
    # print(Status.initiee == Status_bll.initiee)
