from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str
    email: str

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
        orm_mode = True

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
        orm_mode = True