# Monitoring Stack

> **What you'll create:** Set up a complete monitoring stack with Prometheus for metrics collection and Grafana for visualization, monitoring a sample application.

---

## Why Monitoring Matters

### The Problem Without Monitoring

```
┌─────────────────────────────────────────────────────────────────┐
│  WITHOUT MONITORING                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User: "The website is slow!"                                   │
│  You: "Let me check... it looks fine to me?"                    │
│                                                                  │
│  Boss: "Why did the server crash at 3am?"                       │
│  You: "I... don't know. Let me check the logs... somewhere..."  │
│                                                                  │
│  Customer: "My order didn't go through!"                        │
│  You: "I have no idea what happened. Let me restart everything" │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Result: Reactive firefighting, unhappy users, sleepless nights
```

### The Solution With Monitoring

```
┌─────────────────────────────────────────────────────────────────┐
│  WITH MONITORING                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🚨 Alert: "API latency increased to 2.5s (threshold: 1s)"      │
│  You: Fix the slow database query BEFORE users complain         │
│                                                                  │
│  📊 Dashboard shows: CPU spike at 2:50am, memory leak pattern   │
│  You: Deploy fix, explain root cause to boss with data          │
│                                                                  │
│  📈 Metrics show: Payment service error rate 15% at 4:32pm      │
│  You: Find the failed transaction, refund customer, fix bug     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Result: Proactive problem-solving, data-driven decisions, SLA compliance
```

### Real-World Impact

| Scenario | Without Monitoring | With Monitoring |
|----------|-------------------|-----------------|
| **Outage Detection** | Users report after 30+ min | Alert in 30 seconds |
| **Root Cause Analysis** | "I don't know" | "Database connection pool exhausted at 14:32" |
| **Capacity Planning** | Guess and hope | "We'll hit memory limits in 2 weeks at current growth" |
| **Performance Issues** | "Works on my machine" | "P95 latency is 3x higher for /api/search" |
| **Business Decisions** | Gut feeling | "Feature X increased conversion by 12%" |

### Why Every Company Needs Monitoring

- **Amazon**: 100ms of latency = 1% revenue loss
- **Google**: 500ms slower = 20% fewer searches
- **Netflix**: Monitors 2+ billion metrics per day
- **Your Future Employer**: Will expect you to know this!

**Monitoring is not optional** - it's a core DevOps skill that separates junior from senior engineers.

---

## Quick Start

```bash
# 1. Fork and clone this repo

# 2. Complete the configuration files

# 3. Start the stack
docker-compose up -d

# 4. Access dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090

# 5. Push and check your score!
git push origin main
```

---

## What is This Challenge?

You've deployed your application. Now you need to answer:
- Is it running? (uptime)
- How fast is it? (latency)
- Is it overloaded? (resource usage)
- Are there errors? (error rates)

**Monitoring** answers all these questions in real-time!

---

## Do I Need Prior Knowledge?

**You need:**
- ✅ Docker and docker-compose basics
- ✅ Basic understanding of metrics (CPU, memory, etc.)

**You'll learn:**
- What observability means
- Prometheus metrics and PromQL
- Grafana dashboards
- Alerting basics
- The RED and USE methods

---

## What You'll Build

| File | What You Create | Points |
|------|-----------------|--------|
| `prometheus/prometheus.yml` | Prometheus configuration | 20 |
| `grafana/provisioning/` | Grafana data sources | 15 |
| `grafana/dashboards/` | Custom dashboard | 25 |
| `alertmanager/alertmanager.yml` | Alert configuration | 20 |
| `app/` | Instrumented application | 20 |

---

## Step 0: Understand Monitoring Concepts

> ⏱️ **Time:** 20 minutes (reading)

### The Three Pillars of Observability

| Pillar | What It Is | Tools |
|--------|-----------|-------|
| **Metrics** | Numeric measurements over time | Prometheus, DataDog |
| **Logs** | Text records of events | ELK, Loki |
| **Traces** | Request flow through services | Jaeger, Zipkin |

This challenge focuses on **Metrics**.

### What is Prometheus?

**Prometheus** is a time-series database that:
- Scrapes metrics from applications
- Stores them efficiently
- Allows powerful queries (PromQL)
- Triggers alerts

```
Your App ─────► Prometheus ─────► Grafana
   │                │                │
exports metrics    stores         visualizes
on /metrics        data           dashboards
```

### What is Grafana?

**Grafana** is a visualization tool that:
- Connects to data sources (Prometheus, etc.)
- Creates beautiful dashboards
- Supports alerts and annotations
- Allows sharing and collaboration

### The RED Method (Request-focused)

For services, track:
- **R**ate - Requests per second
- **E**rrors - Failed requests
- **D**uration - Response time

### The USE Method (Resource-focused)

For infrastructure, track:
- **U**tilization - % time resource is busy
- **S**aturation - Queue depth
- **E**rrors - Error count

---

## Step 1: Install Docker (if needed)

You should have Docker installed from previous challenges. Verify:

```bash
docker --version
docker-compose --version
```

If not installed, see the Dockerize challenge README.

---

## Step 2: Configure Prometheus

> ⏱️ **Time:** 25-30 minutes

### How Prometheus Works

Prometheus **pulls** metrics from applications:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['app:5000']  # Scrape this endpoint
```

The app exposes metrics at `/metrics`:

```
# Example metrics endpoint output
http_requests_total{method="GET",status="200"} 1234
http_request_duration_seconds{quantile="0.5"} 0.025
process_cpu_seconds_total 45.2
```

### Your Task

Complete `prometheus/prometheus.yml`:

**Requirements:**
- [ ] Set global scrape interval to 15s
- [ ] Add job to scrape Prometheus itself
- [ ] Add job to scrape the sample app
- [ ] Add job to scrape node_exporter (system metrics)

<details>
<summary>💡 Hint 1: Basic Structure</summary>

```yaml
global:
  scrape_interval: 15s      # How often to scrape
  evaluation_interval: 15s  # How often to evaluate rules

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

</details>

<details>
<summary>💡 Hint 2: Multiple Jobs</summary>

```yaml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'app'
    static_configs:
      - targets: ['app:5000']
    metrics_path: /metrics

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'monitoring-challenge'

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Sample application
  - job_name: 'app'
    static_configs:
      - targets: ['app:5000']
    metrics_path: /metrics

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

</details>

---

## Step 3: Configure Grafana Data Sources

> ⏱️ **Time:** 15-20 minutes

### Grafana Provisioning

Grafana can auto-configure data sources from files:

```
grafana/
├── provisioning/
│   ├── datasources/
│   │   └── prometheus.yml    # Data source config
│   └── dashboards/
│       └── dashboards.yml    # Dashboard config
└── dashboards/
    └── app-dashboard.json    # Actual dashboard
```

### Your Task

Complete `grafana/provisioning/datasources/prometheus.yml`:

<details>
<summary>💡 Hint: Data Source Config</summary>

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

</details>

<details>
<summary>🎯 Full Solution</summary>

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: "15s"
      httpMethod: "POST"
```

</details>

---

## Step 4: Create a Grafana Dashboard

> ⏱️ **Time:** 30-40 minutes

### Dashboard Structure

A Grafana dashboard is JSON with panels:

```json
{
  "title": "My Dashboard",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])"
        }
      ]
    }
  ]
}
```

### PromQL Basics

| Query | What It Shows |
|-------|--------------|
| `up` | Is the target up? (1 or 0) |
| `rate(metric[5m])` | Per-second rate over 5 minutes |
| `sum(metric)` | Total across all instances |
| `avg(metric)` | Average across all instances |
| `histogram_quantile(0.95, ...)` | 95th percentile |

### Your Task

Create a dashboard with these panels:
1. Request rate (requests per second)
2. Error rate (% of failed requests)
3. Response time (95th percentile)
4. CPU usage
5. Memory usage

The dashboard JSON goes in `grafana/dashboards/app-dashboard.json`.

<details>
<summary>💡 Hint: Panel Example</summary>

```json
{
  "title": "Request Rate",
  "type": "timeseries",
  "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
  "targets": [
    {
      "expr": "sum(rate(http_requests_total[5m]))",
      "legendFormat": "Requests/sec"
    }
  ]
}
```

</details>

<details>
<summary>🎯 Full Solution</summary>

See `grafana/dashboards/app-dashboard.json` in the solution folder.

Key panels:
- **Request Rate**: `sum(rate(http_requests_total[5m]))`
- **Error Rate**: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100`
- **P95 Latency**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- **CPU**: `rate(process_cpu_seconds_total[5m]) * 100`
- **Memory**: `process_resident_memory_bytes / 1024 / 1024`

</details>

---

## Step 5: Configure Alerting

> ⏱️ **Time:** 25-30 minutes

### Prometheus Alerts

Alerts are defined in rule files:

```yaml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

### Alertmanager

Alertmanager routes and sends alerts:

```yaml
route:
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'default'
    email_configs:
      - to: 'team@example.com'
```

### Your Task

Complete `prometheus/rules/alerts.yml` and `alertmanager/alertmanager.yml`:

**Alert rules to create:**
- [ ] High error rate (> 5%)
- [ ] High response time (> 1s)
- [ ] Service down (target not responding)
- [ ] High CPU usage (> 80%)

<details>
<summary>💡 Hint: Alert Rules</summary>

```yaml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          * 100 > 5
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Error rate above 5%"
          description: "Current error rate: {{ $value }}%"
```

</details>

<details>
<summary>🎯 Full Solution (alerts.yml)</summary>

```yaml
groups:
  - name: app_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          * 100 > 5
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value | printf \"%.2f\" }}s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      - alert: HighCPUUsage
        expr: |
          rate(process_cpu_seconds_total[5m]) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value | printf \"%.2f\" }}%"
```

</details>

---

## Step 6: Instrument the Application

> ⏱️ **Time:** 20-25 minutes

### Prometheus Client Libraries

Most languages have Prometheus client libraries:

```python
# Python example
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total requests', ['method', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')

# Record metrics
REQUEST_COUNT.labels(method='GET', status='200').inc()
with REQUEST_LATENCY.time():
    process_request()

# Expose metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest()
```

### Your Task

The sample app in `app/app.py` needs instrumentation. Add:
- [ ] Request counter (method, status, endpoint)
- [ ] Request duration histogram
- [ ] Active requests gauge
- [ ] /metrics endpoint

<details>
<summary>💡 Hint: Flask Instrumentation</summary>

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'status', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_REQUESTS.inc()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(endpoint=request.endpoint).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        status=response.status_code,
        endpoint=request.endpoint
    ).inc()
    ACTIVE_REQUESTS.dec()
    return response
```

</details>

---

## Step 7: Test Your Stack

### Run the Progress Checker

Before starting the stack, check your configuration files:

```bash
python run.py
```

**Expected output when complete:**
```
============================================================
  📊 Monitoring Stack Challenge
============================================================

  ✅ Prometheus Config (20/20 points)
  ✅ Grafana Datasource (15/15 points)
  ✅ Grafana Dashboard (25/25 points)
  ✅ Alertmanager Config (20/20 points)
  ✅ App Instrumentation (20/20 points)

============================================================
  🎯 Total Score: 100/100
  🎉 CHALLENGE COMPLETE!
============================================================
```

**If you see less than 100:**
- Read the missing items (marked with ✗)
- Check the corresponding step in this README
- Fix your config files and run again

### Start Everything

```bash
docker-compose up -d
```

### Access the UIs

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| App | http://localhost:5000 | - |
| Alertmanager | http://localhost:9093 | - |

### Generate Some Traffic

```bash
# Run this in a loop to generate traffic
for i in {1..100}; do
  curl http://localhost:5000/
  curl http://localhost:5000/api/data
  sleep 0.1
done
```

### Verify Metrics

1. Go to Prometheus: http://localhost:9090
2. Query: `up` - should show all targets as 1
3. Query: `http_requests_total` - should show request counts

### View Dashboard

1. Go to Grafana: http://localhost:3000
2. Login with admin/admin
3. Go to Dashboards → App Dashboard
4. You should see graphs updating!

---

## Understanding Monitoring (For DevOps Students)

### Key Metrics to Monitor

| Category | Metrics | Why |
|----------|---------|-----|
| **Availability** | `up`, error rates | Is it working? |
| **Performance** | Latency, throughput | Is it fast? |
| **Saturation** | CPU, memory, disk | Is it overloaded? |
| **Traffic** | Request rates | How busy is it? |

### PromQL Cheat Sheet

```promql
# Basic queries
up                              # Is target up?
http_requests_total            # Total requests (counter)

# Rates (use with counters)
rate(metric[5m])               # Per-second rate over 5m
irate(metric[5m])              # Instant rate (more spiky)

# Aggregation
sum(metric)                    # Sum across all series
avg(metric)                    # Average
max(metric)                    # Maximum
min(metric)                    # Minimum

# Filtering
metric{label="value"}          # Filter by label
metric{label=~"regex.*"}       # Regex filter
metric{label!="value"}         # Negative filter

# Histograms
histogram_quantile(0.95, rate(metric_bucket[5m]))  # P95
```

### What You Can Say in Interviews

> "I set up a complete monitoring stack using Prometheus and Grafana. I configured Prometheus to scrape metrics from applications and infrastructure using the pull model. I created custom Grafana dashboards following the RED method (Rate, Errors, Duration) for services. I also configured alerting rules for critical conditions like high error rates and latency, with Alertmanager handling alert routing and deduplication."

---

## Troubleshooting

<details>
<summary>❌ Prometheus can't scrape targets</summary>

1. Check target is reachable: `docker exec prometheus wget -qO- http://app:5000/metrics`
2. Check prometheus.yml syntax
3. Verify service names match docker-compose

</details>

<details>
<summary>❌ Grafana shows "No data"</summary>

1. Check data source is configured correctly
2. Verify Prometheus has data: query `up` in Prometheus UI
3. Check time range in Grafana (top right)

</details>

<details>
<summary>❌ Alerts not firing</summary>

1. Check alert rules syntax: Prometheus → Status → Rules
2. Verify expression returns data
3. Check Alertmanager is running: http://localhost:9093

</details>

---

## What You Learned

- ✅ **Observability** - Metrics, logs, traces
- ✅ **Prometheus** - Metrics collection and PromQL
- ✅ **Grafana** - Dashboard creation
- ✅ **Alerting** - Alert rules and routing
- ✅ **Instrumentation** - Adding metrics to apps
- ✅ **RED/USE methods** - What to monitor

---

## Next Steps

This challenge covered **Metrics** (the first pillar of observability). Continue your learning:

| Challenge | Pillar | What You'll Learn |
|-----------|--------|-------------------|
| **[logging-stack](https://github.com/techlearn-center/logging-stack)** | Logs | ELK Stack or Loki + Grafana for centralized logging |
| **[distributed-tracing](https://github.com/techlearn-center/distributed-tracing)** | Traces | Jaeger for request tracing across microservices |

### The Complete Observability Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY STACK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 METRICS (This Challenge)                                    │
│     └── Prometheus + Grafana                                    │
│     └── "What is happening?" (numbers over time)                │
│                                                                  │
│  📝 LOGS (logging-stack)                                        │
│     └── ELK (Elasticsearch, Logstash, Kibana) or Loki           │
│     └── "Why did it happen?" (text records)                     │
│                                                                  │
│  🔗 TRACES (distributed-tracing)                                │
│     └── Jaeger or Zipkin                                        │
│     └── "Where did it happen?" (request flow)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Production-Ready Skills

After completing all three observability challenges, you'll be able to:
- Set up enterprise-grade monitoring infrastructure
- Debug complex distributed systems
- Build SRE/DevOps dashboards
- Configure alerting and on-call rotations
- Talk confidently about observability in interviews

Good luck! 📊
