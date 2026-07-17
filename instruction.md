# Log Report

There is an Apache-style access log at `/app/access.log`. Parse it and write a JSON
summary report to `/app/report.json`.

The report must be a single JSON object with exactly these three keys:

1. `total_requests` — an integer: the total number of request lines in the log.
2. `unique_ips` — an integer: the number of distinct client IP addresses in the log.
3. `top_path` — a string: the request path (e.g. `/index.html`) that appears most
   often across all requests.

Save this JSON object to `/app/report.json`.
