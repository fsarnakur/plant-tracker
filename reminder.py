import sqlite3
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = 1739161848  # Replace with your ID
DB = "plant.db"

def check_needs_water():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT name, last_watered FROM plants 
        WHERE last_watered IS NULL OR date(last_watered) <= date('now', '-3 days')
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "✅ All plants are recently watered."

    msg = "🚨 *Water Reminder!*\nThe following plants need watering:\n"
    for name, date in rows:
        msg += f"• {name} (💧 {date or 'Never'})\n"
    return msg

def send_reminder(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    msg = check_needs_water()
    send_reminder(msg)
