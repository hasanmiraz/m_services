from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # You need to import List from the typing module
from . import models, schemas
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",  # Frontend URL if are using localhost
    "http://localhost:8080",  # Add any other origins want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins (localhost frontend)
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allow all headers (authorization, content-type)
)

@app.get("/users/phone/{phone_number}", response_model=schemas.UserResponse)
def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# 1. Register User
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email
    )
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