import asyncio
from datetime import datetime
from typing import Dict, Optional
import logging
from models import Ticket, TicketStatus, SagaLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SagaOrchestrator:
    def __init__(self):
        self.tickets: Dict[int, Ticket] = {}
        self.saga_logs: Dict[int, list] = {}
        self.id_counter = 1
        self.log_id_counter = 1
        self.max_retries = 3

    async def create_ticket_saga(self, ticket_data: dict) -> Ticket:
        ticket = self._create_ticket(ticket_data)
        
        try:
            if not await self._reserve_seat(ticket):
                await self._compensate_create_ticket(ticket)
                return ticket
            
            if not await self._process_payment(ticket):
                await self._compensate_reservation(ticket)
                return ticket
            
            await self._complete_ticket(ticket)
            
        except Exception as e:
            logger.error(f"Saga failed for ticket {ticket.id}: {str(e)}")
            await self._handle_saga_failure(ticket)
        
        return ticket

    def _create_ticket(self, ticket_data: dict) -> Ticket:
        ticket = Ticket(
            id=self.id_counter,
            **ticket_data,
            status=TicketStatus.NEW,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.tickets[ticket.id] = ticket
        self.id_counter += 1
        
        self._log_saga_step(ticket.id, "CREATE_TICKET", "SUCCESS")
        logger.info(f"Ticket {ticket.id} created with status NEW")
        return ticket

    async def _reserve_seat(self, ticket: Ticket) -> bool:
        try:
            await asyncio.sleep(1)
            
            if hash(f"{ticket.id}_{ticket.seat_number}") % 10 != 0:
                ticket.status = TicketStatus.RESERVED
                ticket.updated_at = datetime.now()
                self._log_saga_step(ticket.id, "RESERVE_SEAT", "SUCCESS")
                logger.info(f"Seat {ticket.seat_number} reserved for ticket {ticket.id}")
                return True
            else:
                raise Exception("Место уже занято")
                
        except Exception as e:
            ticket.status = TicketStatus.FAILED
            ticket.updated_at = datetime.now()
            self._log_saga_step(ticket.id, "RESERVE_SEAT", "FAILED", str(e))
            logger.error(f"Failed to reserve seat for ticket {ticket.id}: {str(e)}")
            return False

    async def _process_payment(self, ticket: Ticket) -> bool:
        try:
            await asyncio.sleep(1)
            
            if hash(f"{ticket.id}_{ticket.price}") % 5 != 0:
                ticket.status = TicketStatus.PAID
                ticket.updated_at = datetime.now()
                self._log_saga_step(ticket.id, "PROCESS_PAYMENT", "SUCCESS")
                logger.info(f"Payment processed for ticket {ticket.id}")
                return True
            else:
                raise Exception("Недостаточно средств")
                
        except Exception as e:
            ticket.status = TicketStatus.FAILED
            ticket.updated_at = datetime.now()
            self._log_saga_step(ticket.id, "PROCESS_PAYMENT", "FAILED", str(e))
            logger.error(f"Payment failed for ticket {ticket.id}: {str(e)}")
            return False

    async def _complete_ticket(self, ticket: Ticket) -> None:
        ticket.status = TicketStatus.DONE
        ticket.updated_at = datetime.now()
        self._log_saga_step(ticket.id, "COMPLETE_TICKET", "SUCCESS")
        logger.info(f"Ticket {ticket.id} completed successfully")

    async def _compensate_create_ticket(self, ticket: Ticket) -> None:
        ticket.status = TicketStatus.CANCELLED
        ticket.updated_at = datetime.now()
        self._log_saga_step(ticket.id, "COMPENSATE_CREATE", "SUCCESS")
        logger.info(f"Ticket {ticket.id} creation compensated (cancelled)")

    async def _compensate_reservation(self, ticket: Ticket) -> None:
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Compensation attempt {attempt + 1} for ticket {ticket.id}")
                
                await asyncio.sleep(1)
                
                ticket.status = TicketStatus.CANCELLED
                ticket.compensation_attempts = attempt + 1
                ticket.updated_at = datetime.now()
                self._log_saga_step(ticket.id, "COMPENSATE_RESERVATION", "SUCCESS", 
                                   f"Attempts: {attempt + 1}")
                logger.info(f"Reservation cancelled for ticket {ticket.id}")
                return
                
            except Exception as e:
                logger.error(f"Compensation attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    ticket.status = TicketStatus.FAILED
                    ticket.updated_at = datetime.now()
                    self._log_saga_step(ticket.id, "COMPENSATE_RESERVATION", "FAILED",
                                       f"Max retries exceeded: {str(e)}")
                    logger.error(f"CRITICAL: Manual intervention needed for ticket {ticket.id}")
                await asyncio.sleep(2 ** attempt)

    async def _handle_saga_failure(self, ticket: Ticket) -> None:
        ticket.status = TicketStatus.FAILED
        ticket.updated_at = datetime.now()
        self._log_saga_step(ticket.id, "SAGA_FAILED", "FAILED", "Critical saga failure")
        logger.error(f"SAGA FAILED for ticket {ticket.id} - MANUAL INTERVENTION REQUIRED")

    def _log_saga_step(self, ticket_id: int, step: str, status: str, error: str = None):
        log = SagaLog(
            id=self.log_id_counter,
            ticket_id=ticket_id,
            step=step,
            status=status,
            timestamp=datetime.now(),
            error_message=error
        )
        
        if ticket_id not in self.saga_logs:
            self.saga_logs[ticket_id] = []
        self.saga_logs[ticket_id].append(log)
        self.log_id_counter += 1

    def get_ticket_status(self, ticket_id: int) -> Optional[Ticket]:
        return self.tickets.get(ticket_id)

    def get_saga_logs(self, ticket_id: int) -> list:
        return self.saga_logs.get(ticket_id, [])
