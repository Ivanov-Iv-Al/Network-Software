from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Tickets Microservice")

class Ticket(BaseModel):
    id: int
    event_name: str
    customer_name: str
    seat_number: str
    price: float
    created_at: datetime

class TicketCreate(BaseModel):
    event_name: str
    customer_name: str
    seat_number: str
    price: float

tickets_db = []
id_counter = 1

@app.post("/api/v1/tickets/", response_model=Ticket, status_code=201)
async def create_ticket(ticket: TicketCreate):
    global id_counter
    new_ticket = Ticket(
        id=id_counter,
        **ticket.model_dump(),
        created_at=datetime.now()
    )
    tickets_db.append(new_ticket)
    id_counter += 1
    return new_ticket

@app.get("/api/v1/tickets/", response_model=List[Ticket])
async def get_tickets():
    return tickets_db

@app.get("/api/v1/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Билет не найден")
    return ticket

@app.delete("/api/v1/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    global tickets_db
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Билет не найден")
    tickets_db = [t for t in tickets_db if t.id != ticket_id]
    return {"message": "Билет удален"}