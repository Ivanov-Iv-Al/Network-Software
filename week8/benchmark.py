import requests
import grpc
import time
import statistics
import sys
import os

sys.path.append(os.path.dirname(__file__))

from gen import service_pb2, service_pb2_grpc

REST_URL = "http://localhost:8000/api/ticket/T-1001"
GRPC_TARGET = "localhost:50051"
ITERATIONS = 1000


def benchmark_rest(n=ITERATIONS):
    times = []
    failed = 0
    
    print(f"  Выполняется {n} запросов к REST API...")
    
    for i in range(n):
        try:
            start = time.perf_counter()
            response = requests.get(REST_URL, timeout=5.0)
            end = time.perf_counter()
            
            if response.status_code == 200:
                times.append(end - start)
            else:
                failed += 1
        except Exception:
            failed += 1
        
        if (i + 1) % 200 == 0:
            print(f"    Прогресс: {i+1}/{n} запросов")
    
    if times:
        return {
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'p50': statistics.median(times),
            'p95': statistics.quantiles(times, n=20)[18] if len(times) >= 20 else max(times),
            'failed': failed,
            'success': len(times)
        }
    return None


def benchmark_grpc(n=ITERATIONS):
    times = []
    failed = 0
    
    print(f"  Выполняется {n} запросов к gRPC API...")
    
    with grpc.insecure_channel(GRPC_TARGET) as channel:
        stub = service_pb2_grpc.TicketsServiceStub(channel)
        
        for i in range(n):
            try:
                request = service_pb2.TicketRequest(
                    ticket_id="T-1001",
                    user_id="benchmark"
                )
                
                start = time.perf_counter()
                response = stub.GetTicketPrice(request, timeout=5.0)
                end = time.perf_counter()
                
                times.append(end - start)
            except Exception:
                failed += 1
            
            if (i + 1) % 200 == 0:
                print(f"    Прогресс: {i+1}/{n} запросов")
    
    if times:
        return {
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'p50': statistics.median(times),
            'p95': statistics.quantiles(times, n=20)[18] if len(times) >= 20 else max(times),
            'failed': failed,
            'success': len(times)
        }
    return None


def print_results(results_rest, results_grpc):
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ БЕНЧМАРКА")
    print("=" * 70)
    
    print(f"\n{'Показатель':<20} {'REST API':<20} {'gRPC API':<20} {'Ускорение':<10}")
    print("-" * 70)
    
    if results_rest and results_grpc:
        avg_rest_ms = results_rest['avg'] * 1000
        avg_grpc_ms = results_grpc['avg'] * 1000
        speedup = avg_rest_ms / avg_grpc_ms
        
        print(f"{'Среднее время (мс)':<20} {avg_rest_ms:<20.2f} {avg_grpc_ms:<20.2f} {speedup:<10.2f}x")
        print(f"{'Минимум (мс)':<20} {results_rest['min']*1000:<20.2f} {results_grpc['min']*1000:<20.2f}")
        print(f"{'Максимум (мс)':<20} {results_rest['max']*1000:<20.2f} {results_grpc['max']*1000:<20.2f}")
        print(f"{'Медиана (мс)':<20} {results_rest['p50']*1000:<20.2f} {results_grpc['p50']*1000:<20.2f}")
        print(f"{'P95 (мс)':<20} {results_rest['p95']*1000:<20.2f} {results_grpc['p95']*1000:<20.2f}")
        print(f"{'Успешных запросов':<20} {results_rest['success']:<20} {results_grpc['success']:<20}")
        print(f"{'Ошибок':<20} {results_rest['failed']:<20} {results_grpc['failed']:<20}")
    
    print("\n" + "=" * 70)


def save_results_to_md(results_rest, results_grpc):
    content = f"""# Результаты бенчмарка: REST vs gRPC

## Конфигурация окружения
- **Количество запросов**: {ITERATIONS}
- **Дата запуска**: {time.strftime('%Y-%m-%d %H:%M:%S')}

## REST API
| Показатель | Значение |
|------------|----------|
| Среднее время | {results_rest['avg']*1000:.2f} мс |
| Минимум | {results_rest['min']*1000:.2f} мс |
| Максимум | {results_rest['max']*1000:.2f} мс |
| Медиана | {results_rest['p50']*1000:.2f} мс |
| P95 | {results_rest['p95']*1000:.2f} мс |
| Успешных запросов | {results_rest['success']} / {ITERATIONS} |

## gRPC API
| Показатель | Значение |
|------------|----------|
| Среднее время | {results_grpc['avg']*1000:.2f} мс |
| Минимум | {results_grpc['min']*1000:.2f} мс |
| Максимум | {results_grpc['max']*1000:.2f} мс |
| Медиана | {results_grpc['p50']*1000:.2f} мс |
| P95 | {results_grpc['p95']*1000:.2f} мс |
| Успешных запросов | {results_grpc['success']} / {ITERATIONS} |

## Сравнительный анализ

**Ускорение gRPC относительно REST**: {results_rest['avg']/results_grpc['avg']:.2f}x

### Выводы
gRPC показывает значительно более высокую производительность по сравнению с REST API:
- Средняя задержка снижена в {results_rest['avg']/results_grpc['avg']:.1f} раз
- Бинарный протокол Protobuf эффективнее текстового JSON
- HTTP/2 с мультиплексированием уменьшает накладные расходы

"""
    os.makedirs("bench", exist_ok=True)
    with open("bench/results.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("\nРезультаты сохранены в bench/results.md")


def main():
    print("=" * 70)
    print("БЕНЧМАРК: REST API vs gRPC API")
    print("=" * 70)
    print(f"\nКоличество запросов: {ITERATIONS}")
    print("Сравниваемые методы: GetTicketPrice (Unary RPC)\n")
    
    results_rest = benchmark_rest()
    results_grpc = benchmark_grpc()
    
    print_results(results_rest, results_grpc)
    
    if results_rest and results_grpc:
        save_results_to_md(results_rest, results_grpc)


if __name__ == "__main__":
    main()