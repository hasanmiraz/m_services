from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:8080",  # Frontend URL if you are using localhost
    "http://localhost:8080",  # Add any other origins you want to allow
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
# 1. Create a User
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

# 2. Get all Users
@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# 3. Create a Tour
@app.post("/tours/", response_model=schemas.TourResponse)
def create_tour(tour: schemas.TourCreate, db: Session = Depends(get_db)):
    new_tour = models.Tour(
        tour_name=tour.tour_name,
        description=tour.description,
        schedule=tour.schedule,
        available_slots=tour.available_slots
    )
    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)
    return new_tour

# 4. Get all Tours
@app.get("/tours/", response_model=List[schemas.TourResponse])
def get_tours(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tours = db.query(models.Tour).offset(skip).limit(limit).all()
    return tours

# 5. Make a Tour Reservation (Check tour and user availability)
@app.post("/tour_reservations/", response_model=schemas.TourReservationResponse)
def make_reservation(reservation: schemas.TourReservationCreate, db: Session = Depends(get_db)):
    tour = db.query(models.Tour).filter(models.Tour.id == reservation.tour_id).first()
    if not tour or tour.available_slots < reservation.number_of_guests:
        raise HTTPException(status_code=400, detail="Not enough slots available")

    user = db.query(models.User).filter(models.User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_reservation = models.TourReservation(
        tour_id=reservation.tour_id,
        user_id=reservation.user_id,
        number_of_guests=reservation.number_of_guests,
        booking_status="confirmed"
    )

    # Reduce available slots after booking
    tour.available_slots -= reservation.number_of_guests
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    db.refresh(tour)

    return new_reservation

# 6. Get all Reservations
@app.get("/tour_reservations/", response_model=List[schemas.TourReservationResponse])
def get_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = db.query(models.TourReservation).offset(skip).limit(limit).all()
    return reservations
