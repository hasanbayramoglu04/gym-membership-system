from datetime import datetime, timedelta
import logging
import os
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gym-dev-secret-key")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

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
            phone TEXT DEFAULT '-',
            plan TEXT NOT NULL,
            end_date TEXT NOT NULL,
            visit_count INTEGER DEFAULT 0,
            last_visit TEXT DEFAULT 'Henuz giris yok'
        )
    """)
  conn.commit()
  conn.close()


# 1. Uye Listeleme ve Durum Kontrolu
@app.route("/")
def index():
  msg = request.args.get("msg", "")
  msg_type = request.args.get("type", "info")

  conn = get_db_connection()
  members_raw = conn.execute("SELECT * FROM members ORDER BY id DESC").fetchall()
  conn.close()

  today_str = datetime.now().strftime("%Y-%m-%d")
  members = []
  for m in members_raw:
    is_active = m["end_date"] >= today_str
    members.append({
        "id": m["id"],
        "name": m["name"],
        "phone": m["phone"],
        "plan": m["plan"],
        "end_date": m["end_date"],
        "visit_count": m["visit_count"],
        "last_visit": m["last_visit"],
        "status": "Aktif" if is_active else "Suresi Dolmus",
        "is_active": is_active,
    })

  return render_template(
      "index.html", members=members, msg=msg, msg_type=msg_type
  )


# 2. Yeni Uye Kaydi
@app.route("/add", methods=["POST"])
def add_member():
  name = request.form.get("name", "").strip()
  phone = request.form.get("phone", "-").strip() or "-"
  plan = request.form.get("plan", "1 Aylik")
  end_date = request.form.get("end_date", "")

  if not name or not end_date:
    return "Ad ve bitis tarihi zorunludur!", 400

  conn = get_db_connection()
  conn.execute(
      "INSERT INTO members (name, phone, plan, end_date) VALUES (?, ?, ?, ?)",
      (name, phone, plan, end_date),
  )
  conn.commit()
  conn.close()
  app.logger.info(f"Yeni uye eklendi: {name} ({plan})")
  return redirect(
      url_for("index", msg=f"{name} basariyla kaydedildi.", type="success")
  )


# 3. Salona Giris Kontrolu (Check-in)
@app.route("/checkin/<int:member_id>", methods=["POST"])
def checkin_member(member_id):
  conn = get_db_connection()
  member = conn.execute(
      "SELECT * FROM members WHERE id = ?", (member_id,)
  ).fetchone()
  if not member:
    conn.close()
    return "Uye bulunamadi", 404

  today_str = datetime.now().strftime("%Y-%m-%d")
  if member["end_date"] < today_str:
    conn.close()
    app.logger.warning(f"Suresi dolmus uye giris denemesi: {member['name']}")
    return redirect(
        url_for(
            "index",
            msg=(
                f"GIRIS REDDEDILDI: {member['name']} adli uyenin suresi"
                " dolmustur!"
            ),
            type="error",
        )
    )

  now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
  new_count = (member["visit_count"] or 0) + 1
  conn.execute(
      "UPDATE members SET visit_count = ?, last_visit = ? WHERE id = ?",
      (new_count, now_str, member_id),
  )
  conn.commit()
  conn.close()
  app.logger.info(
      f"Salona giris yapildi: {member['name']} (Toplam: {new_count})"
  )
  return redirect(
      url_for(
          "index",
          msg=(
              f"{member['name']} salona giris yapti. (Toplam giris:"
              f" {new_count})"
          ),
          type="success",
      )
  )


# 4. Uyelik Suresi Uzatma (+30 Gun)
@app.route("/renew/<int:member_id>", methods=["POST"])
def renew_member(member_id):
  conn = get_db_connection()
  member = conn.execute(
      "SELECT * FROM members WHERE id = ?", (member_id,)
  ).fetchone()
  if member:
    current_end = datetime.strptime(member["end_date"], "%Y-%m-%d")
    base_date = max(current_end, datetime.now())
    new_end = (base_date + timedelta(days=30)).strftime("%Y-%m-%d")
    conn.execute(
        "UPDATE members SET end_date = ? WHERE id = ?", (new_end, member_id)
    )
    conn.commit()
    app.logger.info(f"Uyelik 30 gun uzatildi: {member['name']} -> {new_end}")
  conn.close()
  return redirect(
      url_for("index", msg="Uyelik suresi 30 gun uzatildi.", type="success")
  )


# 5. Uye Kaydi Silme
@app.route("/delete/<int:member_id>", methods=["POST"])
def delete_member(member_id):
  conn = get_db_connection()
  conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
  conn.commit()
  conn.close()
  app.logger.info(f"Uye silindi. ID: {member_id}")
  return redirect(url_for("index", msg="Uye kaydi silindi.", type="info"))


# 6. Sistem Saglik Kontrolu (Health Check)
@app.route("/health")
def health():
  app.logger.info("Health check endpoint cagrildi.")
  return (
      jsonify({
          "status": "healthy",
          "service": "gym-membership-app",
          "version": "1.0",
      }),
      200,
  )


init_db()

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)