import os
import sqlite3
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DB_PATH = os.environ.get("DB_PATH", "gym.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            plan TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM members")
    if cursor.fetchone()[0] == 0:
        today = datetime.now().strftime("%Y-%m-%d")
        next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO members (name, plan, end_date) VALUES (?, ?, ?)", ("Ahmet Yilmaz", "1 Aylik", next_month))
        cursor.execute("INSERT INTO members (name, plan, end_date) VALUES (?, ?, ?)", ("Ayse Demir", "3 Aylik", today))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    members_raw = conn.execute("SELECT * FROM members ORDER BY id DESC").fetchall()
    conn.close()
    today_str = datetime.now().strftime("%Y-%m-%d")
    members = []
    for m in members_raw:
        status = "Aktif" if m["end_date"] >= today_str else "Suresi Dolmus"
        members.append({
            "id": m["id"],
            "name": m["name"],
            "plan": m["plan"],
            "end_date": m["end_date"],
            "status": status
        })
    return render_template("index.html", members=members)

@app.route("/add", methods=["POST"])
def add_member():
    name = request.form.get("name", "").strip()
    plan = request.form.get("plan", "1 Aylik")
    end_date = request.form.get("end_date", "")
    if not name or not end_date:
        return "Ad ve bitis tarihi zorunludur!", 400
    conn = get_db_connection()
    conn.execute("INSERT INTO members (name, plan, end_date) VALUES (?, ?, ?)", (name, plan, end_date))
    conn.commit()
    conn.close()
    app.logger.info(f"Yeni uye eklendi: {name}")
    return redirect(url_for("index"))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
