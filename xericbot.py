
import sqlite3
import base64
import os
import datetime
from telegram.ext import Updater, CommandHandler
from telegram import InputFile

# === CONFIG ===
DB = 'plant.db'
BOT_TOKEN = os.getenv("BOT_TOKEN")  # <-- Replace with your actual token

# === /start ===
def start(update, context):
    update.message.reply_text(
        "🌿 Welcome to Xeric Garden Bot!\n"
        "Available commands:\n"
        "/plants - List all plants\n"
        "/needs_water - Show plants that need watering\n"
        "/plant <id> - View a plant's full info and image\n"
        "/watered <id> - Mark plant as watered today\n"
        "/fertilized <id> - Mark plant as fertilized today\n"
        "/whoami - Get your Telegram user ID"
    )

# === /plants ===
def plants(update, context):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name, last_watered, last_fertilized FROM plants")
    rows = c.fetchall()
    conn.close()

    if not rows:
        update.message.reply_text("📭 No plants found.")
        return

    msg = "🪴 *All Plants:*\n"
    for row in rows:
        msg += f"{row[0]}. {row[1]}\n   💧 {row[2] or '—'} | 🌾 {row[3] or '—'}\n"
    update.message.reply_text(msg)

# === /needs_water ===
def needs_water(update, context):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, last_watered 
        FROM plants 
        WHERE last_watered IS NULL OR date(last_watered) <= date('now', '-3 days')
    """)
    rows = c.fetchall()
    conn.close()

    if rows:
        msg = "🚨 *Needs Watering:*\n"
        for row in rows:
            msg += f"{row[0]}. {row[1]} - 💧 {row[2] or 'Never'}\n"
    else:
        msg = "✅ All plants are recently watered."
    update.message.reply_text(msg)

# === /plant <id> ===
def plant_detail(update, context):
    if not context.args:
        update.message.reply_text("❗Usage: /plant <id>")
        return

    try:
        pid = int(context.args[0])
    except ValueError:
        update.message.reply_text("❗ID must be a number.")
        return

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, code, last_watered, last_fertilized, notes, image_base64
        FROM plants WHERE id = ?
    """, (pid,))
    row = c.fetchone()
    conn.close()

    if not row:
        update.message.reply_text(f"❌ No plant found with ID {pid}")
        return

    msg = (
        f"🌿 *Plant #{row[0]}* - {row[1]}\n"
        f"🆔 Code: `{row[2]}`\n"
        f"💧 Watered: {row[3] or '—'}\n"
        f"🌾 Fertilized: {row[4] or '—'}\n"
        f"📝 Notes: {row[5] or '—'}"
    )
    update.message.reply_text(msg, parse_mode="Markdown")

    if row[6]:  # image_base64 exists
        try:
            image_data = base64.b64decode(row[6])
            image_path = f"/data/data/com.termux/files/usr/tmp/plant_{pid}.jpg"

            with open(image_path, "wb") as f:
                f.write(image_data)

            with open(image_path, "rb") as f:
                update.message.reply_photo(photo=InputFile(f))

            os.remove(image_path)

        except Exception as e:
            update.message.reply_text("⚠️ Image exists but couldn't be sent.")
            print(f"[ERROR] Image decode/send failed: {e}")
    else:
        update.message.reply_text("🖼️ No image stored for this plant.")

# === /watered <id> ===
def update_watered(update, context):
    if not context.args:
        update.message.reply_text("❗Usage: /watered <id>")
        return
    try:
        pid = int(context.args[0])
    except ValueError:
        update.message.reply_text("❗ID must be a number.")
        return

    today = datetime.date.today().isoformat()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE plants SET last_watered = ? WHERE id = ?", (today, pid))
    conn.commit()
    conn.close()

    update.message.reply_text(f"💧 Plant #{pid} marked as watered today ({today})")

# === /fertilized <id> ===
def update_fertilized(update, context):
    if not context.args:
        update.message.reply_text("❗Usage: /fertilized <id>")
        return
    try:
        pid = int(context.args[0])
    except ValueError:
        update.message.reply_text("❗ID must be a number.")
        return

    today = datetime.date.today().isoformat()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE plants SET last_fertilized = ? WHERE id = ?", (today, pid))
    conn.commit()
    conn.close()

    update.message.reply_text(f"🌾 Plant #{pid} marked as fertilized today ({today})")

# === /whoami ===
def whoami(update, context):
    uid = update.message.chat_id
    update.message.reply_text(f"👤 Your Telegram ID: `{uid}`", parse_mode="Markdown")

# === MAIN ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("plants", plants))
    dp.add_handler(CommandHandler("needs_water", needs_water))
    dp.add_handler(CommandHandler("plant", plant_detail))
    dp.add_handler(CommandHandler("watered", update_watered))
    dp.add_handler(CommandHandler("fertilized", update_fertilized))
    dp.add_handler(CommandHandler("whoami", whoami))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
