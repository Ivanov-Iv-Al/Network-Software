import grpc
from concurrent import futures
import sys
import os

sys.path.append(os.path.dirname(__file__))

from gen import service_pb2, service_pb2_grpc


class TicketsServiceServicer(service_pb2_grpc.TicketsServiceServicer):
    
    def GetTicketPrice(self, request, context):
        ticket_prices = {
            "T-1001": {"price": 99.99, "event": "Concert: Rock Night"},
            "T-1002": {"price": 149.99, "event": "Theatre: Hamlet"},
            "T-1003": {"price": 49.99, "event": "Cinema: Dune 2"},
            "T-1004": {"price": 199.99, "event": "Festival: Summer Music"},
            "T-1005": {"price": 299.99, "event": "Opera: La Traviata"},
        }
        
        ticket_info = ticket_prices.get(
            request.ticket_id, 
            {"price": 0.0, "event": "Unknown Event"}
        )
        
        response = service_pb2.TicketResponse(
            ticket_id=request.ticket_id,
            price=ticket_info["price"],
            currency="RUB",
            event_name=ticket_info["event"],
            message=f"Welcome {request.user_id}! Here is your ticket price."
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_TicketsServiceServicer_to_server(
        TicketsServiceServicer(), server
    )
    
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051")
    print("Доступные методы:")
    print("  - GetTicketPrice (Unary RPC)")
    
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.stop(0)


if __name__ == "__main__":
    serve()