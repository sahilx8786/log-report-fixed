import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _compute_expected():
    """Recompute total_requests, unique_ips, and top_path directly from access.log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return total, len(ips), paths.most_common(1)[0][0]


def test_report_exists():
    """Criterion 4: report.json is saved at /app/report.json."""
    assert REPORT_PATH.exists(), "no report.json found"


def test_total_requests():
    """Criterion 1: total_requests equals the actual number of log lines."""
    expected_total, _, _ = _compute_expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("total_requests") == expected_total, (
        f"expected total_requests={expected_total}, got {data.get('total_requests')}"
    )


def test_unique_ips():
    """Criterion 2: unique_ips equals the actual number of distinct client IPs."""
    _, expected_unique_ips, _ = _compute_expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("unique_ips") == expected_unique_ips, (
        f"expected unique_ips={expected_unique_ips}, got {data.get('unique_ips')}"
    )


def test_top_path():
    """Criterion 3: top_path equals the actual most-requested path."""
    _, _, expected_top_path = _compute_expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("top_path") == expected_top_path, (
        f"expected top_path={expected_top_path!r}, got {data.get('top_path')!r}"
    )
