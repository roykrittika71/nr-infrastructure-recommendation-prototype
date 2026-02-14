# Infrastructure Recommendation Prototype

Demo Video: <INSERT VIDEO LINK HERE>

---
## Overview

This prototype demonstrates how PostgreSQL execution telemetry can be transformed into deterministic infrastructure performance recommendations.

While monitoring platforms collect extensive metrics, users still manually derive optimization insights. This system bridges that gap by converting raw query telemetry into validated, explainable recommendations.

---

## Problem Addressed

Database monitoring tools surface query performance metrics but do not proactively recommend optimizations such as missing index detection.

This prototype identifies high-impact query patterns and generates actionable SQL recommendations based on:

- Query frequency
- Cumulative execution time
- Execution plan validation
- Index existence verification

---

## Architecture

The system consists of four components:

1. **Workload Generator (Flask)**
   Simulates real application traffic.

2. **PostgreSQL (AWS RDS)**
   Collects execution telemetry using `pg_stat_statements`.

3. **Recommendation Engine**
   Applies multi-signal validation to detect optimization opportunities.

4. **UI Integration Concept**
   Demonstrates how recommendations would be surfaced within the Infrastructure → Database Entity view.

---

## How It Works

1. Application traffic generates repeated database queries.
2. Telemetry accumulates in `pg_stat_statements`.
3. The engine evaluates execution behavior and infrastructure state.
4. A recommendation is generated only when all validation conditions are met.
5. After applying the fix, the system suppresses redundant recommendations.

---

## Running the Prototype

Install dependencies:

```bash
pip install -r requirements.txt
```

Export environment variables:

```bash
export DB_HOST="your-db-host"
export DB_NAME="nrapp"
export DB_USER="postgres"
export DB_PASSWORD="your-password"
```

Start workload generator:

```bash
python app.py
```

Run recommendation engine:

```bash
python recommendation_engine.py
```

---

## Sample Output

**Missing Index Detected**

```
Infrastructure Recommendations:

Query: SELECT * FROM orders WHERE user_id = $1
Calls: 4756
Total Execution Time: 1963.10 ms
Suggested Action: CREATE INDEX idx_orders_user_id ON orders(user_id);
Confidence Score: 95%
```

**After Index Creation**

```
No actionable recommendations detected.
```

---

## Additional Insights

See `INFRASTRUCTURE_TELEMETRY_LEARNINGS.md` for detailed instrumentation challenges and key learnings.

