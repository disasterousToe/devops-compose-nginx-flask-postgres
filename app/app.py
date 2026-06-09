from flask import Flask, jsonify
import socket
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    return """
    <h1>Hello from Flask App</h1>
    <p>This app is running behind Nginx using Docker Compose.</p>
    <p>Try <a href="/health">/health</a></p>
    <p>Try <a href="/db">/db</a></p>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "flask-app",
        "hostname": socket.gethostname(),
        "environment": os.getenv("APP_ENV", "local")
    })


@app.route("/db")
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("INSERT INTO visits DEFAULT VALUES;")
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM visits;")
        visit_count = cur.fetchone()[0]

        cur.execute("SELECT version();")
        db_version = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "status": "ok",
            "database": "connected",
            "db_host": DB_HOST,
            "visit_count": visit_count,
            "postgres_version": db_version
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "database": "not connected",
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)