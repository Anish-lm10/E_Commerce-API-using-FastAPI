from database import Base
from sqlalchemy import Integer, Column, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType  # for choicess


class User(Base):
    __tablename__ = "user"
    u_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"User: {self.username}"


class Order(Base):

    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIEVERED", "delievered"),
    )

    ORDER_SIZES = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA-LARGE", "extra-large"),
    )

    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    order_size = Column(ChoiceType(choices=ORDER_SIZES), default="MEDIUM")
    user_id = Column(Integer, ForeignKey("user.u_id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order: {self.order_id}"
