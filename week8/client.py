import grpc
import sys
import os

sys.path.append(os.path.dirname(__file__))

from gen import service_pb2, service_pb2_grpc


def run_unary_example(channel):
    stub = service_pb2_grpc.TicketsServiceStub(channel)
    
    request = service_pb2.TicketRequest(
        ticket_id="T-1001",
        user_id="student_331"
    )
    
    try:
        response = stub.GetTicketPrice(request, timeout=5.0)
        print("\n=== Unary RPC Результат ===")
        print(f"Билет: {response.ticket_id}")
        print(f"Мероприятие: {response.event_name}")
        print(f"Цена: {response.price} {response.currency}")
        print(f"Сообщение: {response.message}")
    except grpc.RpcError as e:
        print(f"Ошибка gRPC: {e.code()} - {e.details()}")


def run_streaming_example(channel):
    stub = service_pb2_grpc.TicketsServiceStub(channel)
    
    request = service_pb2.TicketRequest(
        ticket_id="T-1001",
        user_id="stream_user"
    )
    
    print("\n=== Server Streaming RPC ===")
    print("Подписка на обновления цен билета T-1001...")
    print("-" * 40)
    
    try:
        updates = stub.SubscribePriceChanges(request, timeout=30.0)
        
        for update in updates:
            print(f"[{update.update_number}] {update.message} — "
                  f"Новая цена: {update.new_price} RUB "
                  f"(timestamp: {update.timestamp})")
    
    except grpc.RpcError as e:
        print(f"Ошибка gRPC: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("-" * 40)
    print("Поток завершен")


def main():
    target = "localhost:50051"
    print(f"Подключение к gRPC серверу: {target}")
    
    with grpc.insecure_channel(target) as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=3)
            print("Соединение установлено успешно!")
        except grpc.FutureTimeoutError:
            print("Не удалось подключиться к серверу!")
            return
        
        run_unary_example(channel)
        run_streaming_example(channel)


if __name__ == "__main__":
    main()