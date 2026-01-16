"""
Sample Application for Monitoring Challenge
============================================
TODO: Add Prometheus instrumentation to this app!

Requirements:
- Add request counter (method, status, endpoint)
- Add request duration histogram
- Add /metrics endpoint
"""

import os
import time
import random
from flask import Flask, jsonify, request

# TODO: Import prometheus_client
# from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# TODO: Define metrics
# Example:
# REQUEST_COUNT = Counter(
#     'http_requests_total',
#     'Total HTTP requests',
#     ['method', 'status', 'endpoint']
# )
#
# REQUEST_LATENCY = Histogram(
#     'http_request_duration_seconds',
#     'HTTP request latency',
#     ['endpoint'],
#     buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
# )
#
# ACTIVE_REQUESTS = Gauge(
#     'http_requests_active',
#     'Active HTTP requests'
# )


# TODO: Add before_request hook to track active requests and start time
# @app.before_request
# def before_request():
#     request.start_time = time.time()
#     ACTIVE_REQUESTS.inc()


# TODO: Add after_request hook to record metrics
# @app.after_request
# def after_request(response):
#     latency = time.time() - request.start_time
#     REQUEST_LATENCY.labels(endpoint=request.endpoint or 'unknown').observe(latency)
#     REQUEST_COUNT.labels(
#         method=request.method,
#         status=response.status_code,
#         endpoint=request.endpoint or 'unknown'
#     ).inc()
#     ACTIVE_REQUESTS.dec()
#     return response


@app.route("/")
def home():
    """Home endpoint."""
    return jsonify({
        "app": "Monitoring Challenge App",
        "message": "Add Prometheus metrics to this app!",
        "endpoints": {
            "/": "This page",
            "/api/data": "Sample API endpoint",
            "/api/slow": "Slow endpoint (for latency testing)",
            "/api/error": "Error endpoint (for error rate testing)",
            "/health": "Health check",
            "/metrics": "Prometheus metrics (TODO)"
        }
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/api/data")
def api_data():
    """Sample API endpoint."""
    # Simulate some work
    time.sleep(random.uniform(0.01, 0.1))
    return jsonify({
        "data": [1, 2, 3, 4, 5],
        "timestamp": time.time()
    })


@app.route("/api/slow")
def api_slow():
    """Slow endpoint for testing latency alerts."""
    # Simulate slow response
    time.sleep(random.uniform(0.5, 2.0))
    return jsonify({
        "message": "This was slow!",
        "timestamp": time.time()
    })


@app.route("/api/error")
def api_error():
    """Error endpoint for testing error rate alerts."""
    # Randomly fail 50% of the time
    if random.random() < 0.5:
        return jsonify({"error": "Something went wrong!"}), 500
    return jsonify({"message": "Success!"})


# TODO: Add metrics endpoint
# @app.route("/metrics")
# def metrics():
#     """Prometheus metrics endpoint."""
#     return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
