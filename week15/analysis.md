# Performance Analysis Report - Week 15

## Test Environment
- Service: Devices API (port 8106)
- Resource limits: 0.5 CPU, 256MB RAM
- Tool: Custom Python load tester

## Results

| Concurrency | Total Requests | Throughput (RPS) | Avg Latency (ms) | P95 Latency (ms) |
|-------------|----------------|------------------|------------------|------------------|
| 1 | 30 | ~450 | 2.2 | 3.1 |
| 10 | 300 | ~1200 | 8.3 | 12.5 |
| 50 | 1500 | ~2100 | 23.8 | 41.2 |
| 100 | 3000 | ~2450 | 40.7 | 78.3 |

## Analysis

1. **Linear region (1-10 concurrency)**: Latency grows slowly, throughput increases proportionally.
2. **Knee point (~50 concurrency)**: Throughput growth slows down, latency starts increasing faster.
3. **Saturation point (~100 concurrency)**: Throughput plateaus around 2450 RPS, latency spikes significantly (P95 = 78ms).

## Bottleneck
CPU limit (0.5 cores) becomes the bottleneck at high concurrency. The service spends more time context-switching than processing requests.

## Recommendations
- Increase CPU limit to 1 core for production
- Add horizontal scaling (more replicas)
- Implement connection pooling on client side