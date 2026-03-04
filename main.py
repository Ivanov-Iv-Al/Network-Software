from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List
from datetime import datetime
from models import Ticket, TicketCreate, TicketStatus
from saga_orchestrator import SagaOrchestrator

app = FastAPI(title="Tickets Saga Service")
saga_orchestrator = SagaOrchestrator()

@app.post("/api/v1/tickets/", response_model=Ticket, status_code=202)
async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        saga_orchestrator.create_ticket_saga,
        ticket.model_dump()
    )
    
    return Ticket(
        id=saga_orchestrator.id_counter,
        **ticket.model_dump(),
        status=TicketStatus.NEW,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.get("/api/v1/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    ticket = saga_orchestrator.get_ticket_status(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Билет не найден")
    return ticket

@app.get("/api/v1/tickets/{ticket_id}/logs")
async def get_saga_logs(ticket_id: int):
    logs = saga_orchestrator.get_saga_logs(ticket_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Логи не найдены")
    return logs

@app.get("/api/v1/tickets/")
async def get_all_tickets():
    return list(saga_orchestrator.tickets.values())

@app.post("/api/v1/tickets/{ticket_id}/retry-compensation")
async def retry_compensation(ticket_id: int):
    ticket = saga_orchestrator.get_ticket_status(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Билет не найден")
    
    if ticket.status != TicketStatus.FAILED:
        raise HTTPException(status_code=400, detail="Компенсация возможна только для билетов в статусе FAILED")
    
    await saga_orchestrator._compensate_reservation(ticket)
    return {"message": "Compensation retry initiated"}
