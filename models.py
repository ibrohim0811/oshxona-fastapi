from enum import Enum
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    # To'g'ri: Item'dagi 'category' maydoniga bog'lanyapti
    items: Mapped[list["Item"]] = relationship(back_populates="category")


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    about: Mapped[str] = mapped_column(String(500))
    price: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)
    
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    # TO'G'RILANDI: o'zgaruvchi nomi 'category' va back_populates='items' bo'ldi
    category: Mapped["Category"] = relationship(back_populates="items")

    # QO'SHILDI: Order modelidagi 'item' munosabati bilan bog'lanish uchun
    orders: Mapped[list["Order"]] = relationship(back_populates="item")


class StatusChoices(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    DELIVERY = "delivery"
    DELIVERED = "delivered"
    DECLINED = "declined"


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    status: Mapped[StatusChoices] = mapped_column(default=StatusChoices.PENDING)
    
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    # TO'G'RILANDI: Mapped[Item] emas, Mapped[int] bo'lishi kerak
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    
    # To'g'ri: Customer'daging 'orders' maydoniga bog'lanyapti
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    # TO'G'RILANDI: Item klassidagi 'orders' maydoniga bog'lanishi uchun string formatida berildi
    item: Mapped["Item"] = relationship(back_populates="orders")


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(250))
    last_name: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(String(350), unique=True)
    
    # To'g'ri: Order'dagi 'customer' maydoniga bog'lanyapti
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")