from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

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
        orm_mode = True

# Tour schemas
class TourCreate(BaseModel):
    tour_name: str
    description: Optional[str]
    schedule: datetime
    available_slots: int

class TourResponse(BaseModel):
    id: int
    tour_name: str
    description: Optional[str]
    schedule: datetime
    available_slots: int

    class Config:
        orm_mode = True

# Tour Reservation schemas
class TourReservationCreate(BaseModel):
    tour_id: int
    user_id: int
    number_of_guests: int

class TourReservationResponse(BaseModel):
    id: int
    tour: TourResponse
    user: UserResponse
    number_of_guests: int
    booking_status: str

    class Config:
        orm_mode = True
