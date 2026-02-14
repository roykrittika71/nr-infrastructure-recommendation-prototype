from flask import Flask, jsonify
import psycopg2
import os
import random
from prometheus_client import start_http_server, Counter

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/orders")
def get_orders():
    REQUEST_COUNT.inc()
    user_id = random.randint(1, 1000)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({"rows_returned": len(rows)})

if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)
