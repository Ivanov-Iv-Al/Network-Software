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
        print("\n=== Результат Unary RPC вызова ===")
        print(f"Билет: {response.ticket_id}")
        print(f"Мероприятие: {response.event_name}")
        print(f"Цена: {response.price} {response.currency}")
        print(f"Сообщение: {response.message}")
    except grpc.RpcError as e:
        print(f"Ошибка gRPC: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Ошибка: {e}")


def run_multiple_requests(channel):
    stub = service_pb2_grpc.TicketsServiceStub(channel)
    
    tickets = ["T-1001", "T-1002", "T-1003", "T-1004", "T-1005", "T-9999"]
    
    print("\n=== Несколько запросов ===")
    print(f"{'Билет':<10} {'Цена':<10} {'Мероприятие'}")
    print("-" * 40)
    
    for ticket_id in tickets:
        request = service_pb2.TicketRequest(
            ticket_id=ticket_id,
            user_id="batch_user"
        )
        response = stub.GetTicketPrice(request)
        print(f"{response.ticket_id:<10} {response.price:<10.2f} {response.event_name}")


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
        run_multiple_requests(channel)


if __name__ == "__main__":
    main()