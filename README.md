# Infrastructure Recommendation Prototype

## Problem Statement

Monitoring systems collect telemetry but require manual effort to derive actionable performance insights. This prototype converts database telemetry into deterministic infrastructure recommendations.

The system detects high-impact performance issues such as missing indexes and generates explainable recommendations based on real execution data.

---

## Architecture Overview

The system consists of four layers:

1. **Workload Generator (Flask App)**  
   Simulates real application traffic and database queries.

2. **Database (AWS RDS PostgreSQL)**  
   Collects query execution telemetry using `pg_stat_statements`.

3. **Recommendation Engine (Python)**  
   Analyzes query frequency, cumulative execution time, execution plans, and index existence to generate recommendations.

4. **UI Mock (New Relic Integration Concept)**  
   Demonstrates how recommendations would be surfaced within the Infrastructure Database entity view.

---

## How It Works

1. Application traffic generates repeated database queries.
2. PostgreSQL aggregates telemetry using `pg_stat_statements`.
3. The engine detects:
   - High query call frequency
   - High cumulative execution time
   - Sequential scan in execution plan
   - Absence of relevant index
4. A recommendation is generated with a confidence score.
5. After applying the index, the system re-evaluates and suppresses false positives.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Export environment variables

```bash
export DB_HOST="your-db-host"
export DB_NAME="nrapp"
export DB_USER="postgres"
export DB_PASSWORD="your-password"
```

### 3. Start workload generator

```bash
python app.py
```

### 4. Run recommendation engine

```bash
python recommendation_engine.py
```

---

## Sample Output (Broken State)

```
Infrastructure Recommendations:

Query: SELECT * FROM orders WHERE user_id = $1
Calls: 4756
Total Execution Time: 1963.10 ms
Suggested Action: CREATE INDEX idx_orders_user_id ON orders(user_id);
Confidence Score: 95%
```

---

## Sample Output (After Fix)

```
No actionable recommendations detected.
```

---

## Key Design Principles

- Deterministic logic (no black-box AI)
- Explainability
- False positive prevention
- Infrastructure-aware validation
- Entity-centric integration model

