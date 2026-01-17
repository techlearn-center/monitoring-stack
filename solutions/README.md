# Solutions - Monitoring Stack Challenge

> **Warning**: Only look at these solutions if you're stuck! Try to complete the challenge yourself first.

This folder contains complete solution files for reference.

## Solution Files

| File | Description |
|------|-------------|
| `prometheus.yml` | Complete Prometheus configuration with all scrape jobs |
| `app.py` | Complete Flask app with Prometheus metrics instrumentation |

## How to Use Solutions

If you're stuck on a particular task:

1. First, re-read the README.md in the parent folder
2. Try to understand what the configuration should do
3. Look at the solution for hints, not to copy directly
4. Understand WHY the solution works

## Applying Solutions for Testing

To test with solutions:

```bash
# Copy solution files
cp solutions/prometheus.yml prometheus/prometheus.yml
cp solutions/app.py app/app.py

# Rebuild and restart
docker-compose build app
docker-compose up -d

# Generate some traffic
curl http://localhost:5000/api/data
curl http://localhost:5000/api/slow
curl http://localhost:5000/api/error

# Check Prometheus targets at http://localhost:9090/targets
# View metrics in Grafana at http://localhost:3000
```

## Key Learning Points

### Prometheus Configuration (`prometheus.yml`)
- `global.scrape_interval: 15s` - How often to collect metrics
- `scrape_configs` - Define what to monitor:
  - `prometheus` job - Monitor Prometheus itself
  - `app` job - Monitor your application
  - `node` job - Monitor system metrics via node-exporter

### App Instrumentation (`app.py`)
- **Counter** (`http_requests_total`) - Counts events (always increases)
- **Histogram** (`http_request_duration_seconds`) - Measures distributions (latency)
- **Gauge** (`http_requests_active`) - Current value (can go up/down)
- `/metrics` endpoint - Exposes metrics in Prometheus format

## Common PromQL Queries

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m])

# Average latency
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```
