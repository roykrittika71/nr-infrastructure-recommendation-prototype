import psycopg2
import os

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

CALL_THRESHOLD = 1000
TIME_THRESHOLD = 100


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"
    )


def index_exists(cursor):
    cursor.execute("""
        SELECT 1
        FROM pg_indexes
        WHERE tablename = 'orders'
        AND indexdef LIKE '%user_id%';
    """)
    return cursor.fetchone() is not None


def detect_sequential_scan(cursor):
    cursor.execute("""
        EXPLAIN
        SELECT * FROM orders WHERE user_id = 42;
    """)
    plan = cursor.fetchall()
    for row in plan:
        if "Seq Scan" in row[0]:
            return True
    return False


def analyze_queries():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT query, calls, total_exec_time
        FROM pg_stat_statements
        WHERE query LIKE '%orders%'
        ORDER BY total_exec_time DESC;
    """)

    rows = cur.fetchall()
    recommendations = []

    has_index = index_exists(cur)
    is_seq_scan = detect_sequential_scan(cur)

    for query, calls, total_exec_time in rows:
        if calls > CALL_THRESHOLD and total_exec_time > TIME_THRESHOLD:
            if is_seq_scan and not has_index:
                recommendations.append({
                    "query": query,
                    "calls": calls,
                    "total_exec_time": total_exec_time,
                    "recommendation": "CREATE INDEX idx_orders_user_id ON orders(user_id);",
                    "confidence": 95
                })

    cur.close()
    conn.close()
    return recommendations


if __name__ == "__main__":
    recs = analyze_queries()

    if not recs:
        print("No actionable recommendations detected.")
    else:
        print("\nInfrastructure Recommendations:\n")
        for r in recs:
            print(f"Query: {r['query']}")
            print(f"Calls: {r['calls']}")
            print(f"Total Execution Time: {r['total_exec_time']:.2f} ms")
            print(f"Suggested Action: {r['recommendation']}")
            print(f"Confidence Score: {r['confidence']}%")
            print("-" * 60)

