from pydantic import BaseModel
from datetime import datetime
from typing import List

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

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    total_price: float

class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    total_price: float
    booking_status: str

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    room_type: str
    price_per_night: float
    availability_status: str = "available"

class RoomResponse(BaseModel):
    id: int
    room_type: str
    price_per_night: float
    availability_status: str

    class Config:
        from_attributes = True