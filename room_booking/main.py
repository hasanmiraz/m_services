from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # You need to import List from the typing module
from . import models, schemas
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Register User
@app.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. Book a Room
@app.post("/rooms/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    new_room = models.Room(
        room_type=room.room_type,
        price_per_night=room.price_per_night,
        availability_status=room.availability_status
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# 2. Get All Rooms
@app.get("/rooms/", response_model=List[schemas.RoomResponse])
def get_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = db.query(models.Room).offset(skip).limit(limit).all()
    return rooms

# 3. Book a Room (with room availability check)
@app.post("/bookings/", response_model=schemas.BookingResponse)
def book_room(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    room = db.query(models.Room).filter(models.Room.id == booking.room_id).first()
    if not room or room.availability_status != "available":
        raise HTTPException(status_code=400, detail="Room not available")

    # Create the booking
    new_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=booking.total_price,
        booking_status="confirmed"
    )
    
    # Mark room as booked
    room.availability_status = "booked"
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    db.refresh(room)

    return new_booking

# 4. Get all bookings
@app.get("/bookings/", response_model=List[schemas.BookingResponse])
def get_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).offset(skip).limit(limit).all()
    return bookings