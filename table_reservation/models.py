from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    reservations = relationship("Reservation", back_populates="user")

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, index=True)
    capacity = Column(Integer)
    availability_status = Column(String, default="available")  # "available" or "booked"

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, nullable=False)
    time = Column(DateTime, nullable=False)
    number_of_guests = Column(Integer)
    special_requests = Column(String, nullable=True)
    reservation_status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

    table = relationship("Table")
    user = relationship("User", back_populates="reservations")
