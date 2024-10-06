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

# 3. Create a Table
@app.post("/tables/", response_model=schemas.TableResponse)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    new_table = models.Table(
        restaurant_name=table.restaurant_name,
        capacity=table.capacity,
        availability_status=table.availability_status
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

# 4. Get all Tables
@app.get("/tables/", response_model=List[schemas.TableResponse])
def get_tables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tables = db.query(models.Table).offset(skip).limit(limit).all()
    return tables

# 5. Make a Reservation (Check table and user availability)
@app.post("/reservations/", response_model=schemas.ReservationResponse)
def make_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == reservation.table_id).first()
    if not table or table.availability_status != "available":
        raise HTTPException(status_code=400, detail="Table not available")

    user = db.query(models.User).filter(models.User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_reservation = models.Reservation(
        table_id=reservation.table_id,
        user_id=reservation.user_id,
        date=reservation.date,
        time=reservation.time,
        number_of_guests=reservation.number_of_guests,
        special_requests=reservation.special_requests,
        reservation_status="confirmed"
    )
    
    table.availability_status = "booked"
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    db.refresh(table)

    return new_reservation

# 6. Get all Reservations
@app.get("/reservations/", response_model=List[schemas.ReservationResponse])
def get_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = db.query(models.Reservation).offset(skip).limit(limit).all()
    return reservations
