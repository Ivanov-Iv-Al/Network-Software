import time
import threading
import requests
from collections import defaultdict

URL = "http://localhost:8106/api/devices"

def worker(concurrency_id, results, num_requests=100):
    times = []
    for _ in range(num_requests):
        start = time.perf_counter()
        try:
            resp = requests.get(URL, timeout=5)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
        except:
            pass
    results[concurrency_id] = times

def run_test(concurrency, requests_per_thread=50):
    threads = []
    results = defaultdict(list)
    start_time = time.perf_counter()
    for i in range(concurrency):
        t = threading.Thread(target=worker, args=(i, results, requests_per_thread))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    total_time = time.perf_counter() - start_time
    all_times = [t for sublist in results.values() for t in sublist]
    avg_latency = sum(all_times) / len(all_times) if all_times else 0
    throughput = len(all_times) / total_time
    return {
        "concurrency": concurrency,
        "total_requests": len(all_times),
        "avg_latency_ms": round(avg_latency, 2),
        "throughput_rps": round(throughput, 2),
        "p95_latency": round(sorted(all_times)[int(len(all_times)*0.95)], 2) if all_times else 0
    }

if __name__ == "__main__":
    print("=== Performance Analysis (Week 15) ===")
    for c in [1, 10, 50, 100]:
        res = run_test(c, requests_per_thread=30)
        print(f"Concurrency: {res['concurrency']} | RPS: {res['throughput_rps']} | Avg Latency: {res['avg_latency_ms']}ms | P95: {res['p95_latency']}ms")