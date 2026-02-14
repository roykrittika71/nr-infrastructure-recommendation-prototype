# Aha Moments and Instrumentation Challenges

## Objective

This section focuses specifically on insights and challenges encountered while preparing instrumentation and dataset readiness for building the recommendation prototype.

---

# Aha Moments

## 1. Telemetry Availability Is Not Equal to Telemetry Usability

Although PostgreSQL exposes query statistics through `pg_stat_statements`, it does not automatically translate into actionable insights. Raw metrics such as execution count and cumulative time require contextual validation (e.g., execution plan analysis) before they can support recommendations.

Insight:
Effective recommendations require combining multiple signals rather than relying on a single telemetry dimension.

---

## 2. Execution Plan Validation Is Critical for Accuracy

High cumulative execution time alone does not imply a missing index. Without validating whether the query is performing a sequential scan, recommendations could be incorrect.

Insight:
Telemetry must be paired with execution plan inspection to reduce false positives.

---

## 3. Historical Aggregation Persists After Infrastructure Fixes

After creating an index, `pg_stat_statements` continued to show high cumulative execution time because it stores historical aggregates.

Insight:
Recommendation systems must evaluate current infrastructure state in addition to historical telemetry.

This directly influenced the decision to validate execution plans dynamically before generating recommendations.

---

## 4. Instrumentation Requires Explicit Enablement

`pg_stat_statements` is not enabled by default in RDS. Enabling it required:
- Creating a custom DB parameter group
- Updating the instance configuration
- Rebooting the database instance

Insight:
Observability readiness depends on infrastructure configuration maturity. Telemetry collection is not always plug-and-play.

---

## 5. Network Configuration Affects Data Accessibility

Initial security group configuration prevented external access to the database instance.

Insight:
Instrumentation data may exist but remain inaccessible without correct network permissions.

Observability is dependent on proper security and networking configuration.

---

# Problems Identified During Dataset Preparation

## 1. Default Parameter Groups Cannot Be Edited

The default RDS parameter group is immutable. A custom parameter group had to be created to enable required extensions.

Impact:
Delayed instrumentation setup and required instance restart.

---

## 2. Inbound Rule Misconfiguration

Attempting to add CIDR rules to an existing referenced security group resulted in configuration errors.

Impact:
Connection failures and authentication confusion.

---

## 3. Sequential Scan Detection Required Manual Validation

Telemetry tables do not directly indicate index absence. Execution plan parsing was necessary.

Impact:
Additional logic required beyond simple telemetry aggregation.

---

## 4. Telemetry Noise and System Queries

System-generated queries (e.g., heartbeat queries, metadata checks) appeared in `pg_stat_statements`.

Impact:
Filtering was required to isolate relevant workload queries.

---

## 5. Environment Reproducibility Concerns

Initial hardcoded credentials and dependency inconsistencies highlighted the importance of:
- Environment variables
- Dependency freezing (`requirements.txt`)
- Clean repository hygiene

Impact:
Instrumentation and dataset readiness must include reproducibility discipline.

---

# Summary Insight

The process revealed that building an infrastructure recommendation system requires more effort in instrumentation validation and dataset conditioning than in algorithm design.

The primary complexity lies in:

- Enabling telemetry
- Ensuring signal quality
- Validating execution behavior
- Avoiding false positives
- Maintaining infrastructure state awareness

The intelligence layer is only as reliable as the instrumentation layer beneath it.

