cat > connection.py <<'EOF'
import psycopg2
import os

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "activityhub"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin")
    )
    return conn

def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print(f"Connection successful! Result: {result}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
EOF
