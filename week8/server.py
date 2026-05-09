import grpc
from concurrent import futures
import time
import random
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
            message=f"Welcome {request.user_id}!"
        )
        return response
    
    def SubscribePriceChanges(self, request, context):
        ticket_id = request.ticket_id
        user_id = request.user_id
        
        print(f"[Stream] Новый подписчик: user={user_id}, ticket={ticket_id}")
        
        for i in range(15):
            price_change = random.uniform(-10, 15)
            current_price = 99.99 + sum(random.uniform(-5, 10) for _ in range(i))
            current_price = max(10, round(current_price + price_change, 2))
            
            update = service_pb2.PriceUpdate(
                ticket_id=ticket_id,
                new_price=current_price,
                timestamp=int(time.time()),
                message=f"Price update #{i+1}: {'↑' if price_change > 0 else '↓'}",
                update_number=i + 1
            )
            
            print(f"[Stream] Отправка обновления #{i+1} для {ticket_id}: {current_price} RUB")
            yield update
            time.sleep(0.5)
        
        print(f"[Stream] Завершение потока для {ticket_id}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_TicketsServiceServicer_to_server(
        TicketsServiceServicer(), server
    )
    
    server.add_insecure_port('[::]:50051')
    print("=" * 50)
    print("gRPC сервер запущен на порту 50051")
    print("Доступные методы:")
    print("  - GetTicketPrice (Unary RPC)")
    print("  - SubscribePriceChanges (Server Streaming RPC)")
    print("=" * 50)
    
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.stop(0)


if __name__ == "__main__":
    serve()