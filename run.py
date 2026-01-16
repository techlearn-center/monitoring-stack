#!/usr/bin/env python3
"""
Monitoring Stack Challenge Runner
==================================
Run this script to check your configuration files and see your progress.

Usage:
    python run.py           # Check all config files
    python run.py --start   # Start the stack with docker-compose
    python run.py --stop    # Stop the stack
"""

import subprocess
import sys
import os
import json
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# For Windows compatibility
if sys.platform == 'win32':
    os.system('color')


def print_header():
    """Print the challenge header."""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  📊 Monitoring Stack Challenge{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")


def load_file_content(file_path):
    """Load file content."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def check_prometheus_config(content):
    """Check prometheus.yml for required elements."""
    checks = []
    points = 0
    max_points = 20

    if content is None:
        return [("prometheus.yml exists", False, "File not found")], 0, max_points

    # Check scrape_interval
    if 'scrape_interval: 15s' in content:
        checks.append(("Scrape interval 15s", True, "Configured"))
        points += 4
    elif 'scrape_interval:' in content:
        checks.append(("Scrape interval 15s", False, "Wrong value"))
        points += 2
    else:
        checks.append(("Scrape interval 15s", False, "Missing"))

    # Check alertmanager
    if 'alertmanagers:' in content and '# alertmanagers' not in content.split('alertmanagers:')[0][-20:]:
        checks.append(("Alertmanager config", True, "Configured"))
        points += 4
    else:
        checks.append(("Alertmanager config", False, "Missing or commented"))

    # Check scrape jobs
    jobs = ['prometheus', 'app', 'node']
    for job in jobs:
        pattern = f"job_name: '{job}'"
        alt_pattern = f'job_name: "{job}"'
        if (pattern in content or alt_pattern in content) and f"# {pattern}" not in content:
            checks.append((f"Job: {job}", True, "Configured"))
            points += 4
        else:
            checks.append((f"Job: {job}", False, "Missing or commented"))

    return checks, points, max_points


def check_alertmanager_config(content):
    """Check alertmanager.yml for required elements."""
    checks = []
    points = 0
    max_points = 20

    if content is None:
        return [("alertmanager.yml exists", False, "File not found")], 0, max_points

    # Check route
    if 'route:' in content:
        checks.append(("Route configured", True, ""))
        points += 5
    else:
        checks.append(("Route configured", False, "Missing"))

    # Check receivers
    if 'receivers:' in content:
        checks.append(("Receivers defined", True, ""))
        points += 5
    else:
        checks.append(("Receivers defined", False, "Missing"))

    # Check group_by
    if 'group_by:' in content:
        checks.append(("Group by configured", True, ""))
        points += 5
    else:
        checks.append(("Group by configured", False, "Missing"))

    # Check inhibit_rules
    if 'inhibit_rules:' in content:
        checks.append(("Inhibit rules", True, ""))
        points += 5
    else:
        checks.append(("Inhibit rules", False, "Missing"))

    return checks, points, max_points


def check_grafana_datasource(content):
    """Check Grafana datasource config."""
    checks = []
    points = 0
    max_points = 15

    if content is None:
        return [("datasource config exists", False, "File not found")], 0, max_points

    # Check datasource definition
    if 'datasources:' in content and '# datasources' not in content.split('datasources:')[0][-5:]:
        checks.append(("Datasources defined", True, ""))
        points += 3
    else:
        checks.append(("Datasources defined", False, "Missing or commented"))

    # Check prometheus type
    if 'type: prometheus' in content and '# type: prometheus' not in content:
        checks.append(("Prometheus type", True, ""))
        points += 4
    else:
        checks.append(("Prometheus type", False, "Missing or commented"))

    # Check URL
    if 'url: http://prometheus:9090' in content or 'url: "http://prometheus:9090"' in content:
        checks.append(("Prometheus URL", True, ""))
        points += 4
    else:
        checks.append(("Prometheus URL", False, "Missing or wrong"))

    # Check isDefault
    if 'isDefault: true' in content:
        checks.append(("Is default", True, ""))
        points += 4
    else:
        checks.append(("Is default", False, "Missing"))

    return checks, points, max_points


def check_dashboard(content):
    """Check Grafana dashboard JSON."""
    checks = []
    points = 0
    max_points = 25

    if content is None:
        return [("dashboard.json exists", False, "File not found")], 0, max_points

    try:
        dashboard = json.loads(content)
    except json.JSONDecodeError:
        return [("Valid JSON", False, "Invalid JSON")], 0, max_points

    checks.append(("Valid JSON", True, ""))
    points += 5

    # Check panels
    panels = dashboard.get('panels', [])
    if len(panels) >= 4:
        checks.append(("4+ panels", True, f"{len(panels)} panels"))
        points += 5
    else:
        checks.append(("4+ panels", False, f"Only {len(panels)} panels"))

    # Check for PromQL queries (not placeholders)
    has_real_queries = False
    placeholder_count = 0
    for panel in panels:
        targets = panel.get('targets', [])
        for target in targets:
            expr = target.get('expr', '')
            if 'REPLACE_WITH' in expr:
                placeholder_count += 1
            elif expr and expr != '':
                has_real_queries = True

    if has_real_queries and placeholder_count == 0:
        checks.append(("Real PromQL queries", True, "All panels have queries"))
        points += 10
    elif has_real_queries:
        checks.append(("Real PromQL queries", False, f"{placeholder_count} placeholders remaining"))
        points += 5
    else:
        checks.append(("Real PromQL queries", False, "No real queries"))

    # Check title
    if dashboard.get('title') and dashboard['title'] != 'App Dashboard':
        checks.append(("Custom title", True, dashboard['title']))
        points += 5
    else:
        checks.append(("Custom title", False, "Using default title"))
        points += 2  # Partial credit

    return checks, points, max_points


def check_alerts(content):
    """Check alert rules."""
    checks = []
    points = 0
    max_points = 20

    if content is None:
        return [("alerts.yml exists", False, "File not found")], 0, max_points

    # Check for uncommented alerts
    alert_names = ['HighErrorRate', 'HighLatency', 'ServiceDown', 'HighCPUUsage']
    for alert in alert_names:
        # Check if alert exists and is not commented
        if f'alert: {alert}' in content:
            # Check if it's not in a comment
            lines = content.split('\n')
            is_uncommented = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if f'alert: {alert}' in line:
                    is_uncommented = True
                    break

            if is_uncommented:
                checks.append((f"Alert: {alert}", True, "Configured"))
                points += 5
            else:
                checks.append((f"Alert: {alert}", False, "Commented out"))
        else:
            checks.append((f"Alert: {alert}", False, "Missing"))

    return checks, points, max_points


def check_app_instrumentation(content):
    """Check app instrumentation."""
    checks = []
    points = 0
    max_points = 20

    if content is None:
        return [("app.py exists", False, "File not found")], 0, max_points

    # Check prometheus_client import
    if 'from prometheus_client import' in content and '# from prometheus_client' not in content:
        checks.append(("Prometheus client import", True, ""))
        points += 4
    else:
        checks.append(("Prometheus client import", False, "Missing or commented"))

    # Check Counter
    if 'Counter(' in content and '# Counter(' not in content:
        checks.append(("Request counter", True, ""))
        points += 4
    else:
        checks.append(("Request counter", False, "Missing or commented"))

    # Check Histogram
    if 'Histogram(' in content and '# Histogram(' not in content:
        checks.append(("Request histogram", True, ""))
        points += 4
    else:
        checks.append(("Request histogram", False, "Missing or commented"))

    # Check metrics endpoint
    if '@app.route("/metrics")' in content and '# @app.route("/metrics")' not in content:
        checks.append(("Metrics endpoint", True, ""))
        points += 4
    else:
        checks.append(("Metrics endpoint", False, "Missing or commented"))

    # Check generate_latest
    if 'generate_latest()' in content and '# generate_latest()' not in content:
        checks.append(("Generate latest", True, ""))
        points += 4
    else:
        checks.append(("Generate latest", False, "Missing or commented"))

    return checks, points, max_points


def check_all_configs():
    """Check all configuration files."""
    print_header()
    print(f"  {Colors.BOLD}Checking your monitoring stack...{Colors.END}\n")

    project_dir = Path(__file__).parent

    total_points = 0
    max_total = 0

    config_checks = [
        ("prometheus/prometheus.yml", "Prometheus Config", check_prometheus_config, 20),
        ("alertmanager/alertmanager.yml", "Alertmanager", check_alertmanager_config, 20),
        ("grafana/provisioning/datasources/prometheus.yml", "Grafana Datasource", check_grafana_datasource, 15),
        ("grafana/dashboards/app-dashboard.json", "Grafana Dashboard", check_dashboard, 25),
        ("prometheus/rules/alerts.yml", "Alert Rules", check_alerts, 20),
    ]

    for filepath, display_name, check_func, max_pts in config_checks:
        file_path = project_dir / filepath
        content = load_file_content(file_path)
        checks, points, max_points = check_func(content)

        total_points += points
        max_total += max_points

        # Print results
        status_icon = f"{Colors.GREEN}✅{Colors.END}" if points == max_points else f"{Colors.YELLOW}⏳{Colors.END}"
        print(f"  {status_icon} {Colors.BOLD}{display_name}{Colors.END} ({points}/{max_points} points)")

        for check_name, passed, detail in checks:
            icon = f"{Colors.GREEN}✓{Colors.END}" if passed else f"{Colors.RED}✗{Colors.END}"
            detail_str = f" - {detail}" if detail else ""
            print(f"      {icon} {check_name}{detail_str}")

        print()

    # Progress bar
    progress_pct = int((total_points / max_total) * 100) if max_total > 0 else 0
    bar_filled = int(progress_pct / 5)
    bar_empty = 20 - bar_filled

    bar_color = Colors.GREEN if progress_pct >= 80 else Colors.YELLOW
    print(f"  {Colors.BOLD}Score:{Colors.END}")
    print(f"  {bar_color}{'█' * bar_filled}{'░' * bar_empty}{Colors.END} {total_points}/{max_total} points ({progress_pct}%)")

    if progress_pct == 100:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}🎉 All configs complete!{Colors.END}")
        print(f"  {Colors.CYAN}Run 'python run.py --start' to launch the stack!{Colors.END}")
    elif progress_pct >= 80:
        print(f"\n  {Colors.GREEN}Almost there! Check the items marked with ✗{Colors.END}")
    else:
        print(f"\n  {Colors.CYAN}Keep going! See README.md for guidance.{Colors.END}")

    print()
    return progress_pct == 100


def start_stack():
    """Start the monitoring stack."""
    print_header()
    print(f"  {Colors.BOLD}Starting monitoring stack...{Colors.END}\n")

    project_dir = Path(__file__).parent

    result = subprocess.run(
        ["docker-compose", "up", "-d"],
        cwd=str(project_dir)
    )

    if result.returncode == 0:
        print(f"\n  {Colors.GREEN}✅ Stack started!{Colors.END}")
        print(f"\n  {Colors.CYAN}Access the UIs:{Colors.END}")
        print(f"  • Grafana:      http://localhost:3000 (admin/admin)")
        print(f"  • Prometheus:   http://localhost:9090")
        print(f"  • App:          http://localhost:5000")
        print(f"  • Alertmanager: http://localhost:9093")
    else:
        print(f"\n  {Colors.RED}❌ Failed to start stack{Colors.END}")

    print()


def stop_stack():
    """Stop the monitoring stack."""
    print_header()
    print(f"  {Colors.BOLD}Stopping monitoring stack...{Colors.END}\n")

    project_dir = Path(__file__).parent

    subprocess.run(
        ["docker-compose", "down"],
        cwd=str(project_dir)
    )

    print(f"\n  {Colors.GREEN}✅ Stack stopped{Colors.END}\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Monitoring Stack Challenge Runner")
    parser.add_argument("--start", action="store_true", help="Start the monitoring stack")
    parser.add_argument("--stop", action="store_true", help="Stop the monitoring stack")

    args = parser.parse_args()

    os.chdir(Path(__file__).parent)

    if args.start:
        start_stack()
    elif args.stop:
        stop_stack()
    else:
        check_all_configs()


if __name__ == "__main__":
    main()
