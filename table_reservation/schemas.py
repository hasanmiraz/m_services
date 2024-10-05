from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True

# Table schemas
class TableCreate(BaseModel):
    restaurant_name: str
    capacity: int
    availability_status: str = "available"

class TableResponse(BaseModel):
    id: int
    restaurant_name: str
    capacity: int
    availability_status: str

    class Config:
        from_attributes = True

# Reservation schemas
class ReservationCreate(BaseModel):
    table_id: int
    user_id: int
    date: datetime
    time: datetime
    number_of_guests: int
    special_requests: Optional[str]

class ReservationResponse(BaseModel):
    id: int
    table_id: int
    user: UserResponse
    date: datetime
    time: datetime
    number_of_guests: int
    special_requests: Optional[str]
    reservation_status: str

    class Config:
        from_attributes = True
