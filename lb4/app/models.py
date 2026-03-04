from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TicketStatus(str, Enum):
    NEW = "NEW"
    RESERVED = "RESERVED"
    PAID = "PAID"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class Ticket(BaseModel):
    id: int
    event_name: str
    customer_name: str
    seat_number: str
    price: float
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    compensation_attempts: int = 0

class TicketCreate(BaseModel):
    event_name: str
    customer_name: str
    seat_number: str
    price: float

class SagaLog(BaseModel):
    id: int
    ticket_id: int
    step: str
    status: str
    timestamp: datetime
    error_message: Optional[str] = None