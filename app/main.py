from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    conn = sqlite3.connect("db.sqlite")
    # Vulnerable to SQL injection (demo)
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    return conn.execute(query).fetchall()
