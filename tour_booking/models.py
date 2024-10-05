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

    reservations = relationship("TourReservation", back_populates="user")


class Tour(Base):
    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True, index=True)
    tour_name = Column(String, nullable=False)
    description = Column(String)
    schedule = Column(DateTime, nullable=False)
    available_slots = Column(Integer, nullable=False)


class TourReservation(Base):
    __tablename__ = 'tour_reservations'

    id = Column(Integer, primary_key=True, index=True)
    tour_id = Column(Integer, ForeignKey('tours.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    number_of_guests = Column(Integer)
    booking_status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

    tour = relationship("Tour")
    user = relationship("User", back_populates="reservations")
