import requests
import os
from dotenv import load_dotenv
from sheets import save_reservation
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

load_dotenv()

INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
TOKEN = os.getenv("ULTRAMSG_TOKEN")

# Store conversation state
user_sessions = {}

FAQS = {
    "hours": "🕐 Fork & Flame is open:\nMon-Fri: 11AM - 11PM\nSat-Sun: 10AM - 12AM",
    "location": "📍 123 Flame Street, London, UK\nGoogle Maps: https://maps.google.com",
    "menu": "🍽️ View our full menu here: https://forknflame.com/menu",
    "vegetarian": "🥗 Yes! We have a dedicated vegetarian menu. Ask our staff for details.",
    "parking": "🚗 Free parking available behind the restaurant.",
    "wifi": "📶 Free WiFi available. Password given at the table."
}

scheduler = BackgroundScheduler()
scheduler.start()

def send_message(to, message):
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    payload = {
        "token": TOKEN,
        "to": to,
        "body": message
    }
    requests.post(url, data=payload)

def send_review_request(to):
    message = (
        "🍽️ Thank you for dining at Fork & Flame!\n\n"
        "We hope you had an amazing experience. "
        "Would you mind leaving us a quick Google review? "
        "It means the world to us! ⭐⭐⭐⭐⭐\n\n"
        "👉 https://g.page/forknflame/review"
    )
    send_message(to, message)

def schedule_review(to, reservation_time):
    run_time = reservation_time + timedelta(hours=2)
    scheduler.add_job(
        send_review_request,
        'date',
        run_date=run_time,
        args=[to]
    )

def handle_message(sender, message):
    # FAQ checks
    if "hour" in message or "open" in message or "timing" in message:
        send_message(sender, FAQS["hours"])
        return

    if "location" in message or "address" in message or "where" in message:
        send_message(sender, FAQS["location"])
        return

    if "menu" in message or "food" in message or "dish" in message:
        send_message(sender, FAQS["menu"])
        return

    if "vegetarian" in message or "vegan" in message:
        send_message(sender, FAQS["vegetarian"])
        return

    if "parking" in message or "park" in message:
        send_message(sender, FAQS["parking"])
        return

    if "wifi" in message or "internet" in message:
        send_message(sender, FAQS["wifi"])
        return

    # Reservation flow
    if "book" in message or "reserve" in message or "reservation" in message or "table" in message:
        user_sessions[sender] = {"step": "party_size"}
        send_message(sender,
            "🍽️ Welcome to Fork & Flame! Let's get your table reserved.\n\n"
            "How many people will be dining?"
        )
        return

    # Handle reservation steps
    if sender in user_sessions:
        session = user_sessions[sender]

        if session["step"] == "party_size":
            session["party_size"] = message
            session["step"] = "date"
            send_message(sender, "📅 What date would you like? (e.g. 25 June 2026)")
            return

        if session["step"] == "date":
            session["date"] = message
            session["step"] = "time"
            send_message(sender, "🕐 What time would you like? (e.g. 7:30 PM)")
            return

        if session["step"] == "time":
            session["time"] = message
            session["step"] = "name"
            send_message(sender, "👤 What name should we put the reservation under?")
            return

        if session["step"] == "name":
            session["name"] = message
            session["step"] = "done"

            # Save to Google Sheets
            save_reservation(
                session["name"],
                sender,
                session["party_size"],
                session["date"],
                session["time"]
            )

            # Schedule review request
            reservation_datetime = datetime.now() + timedelta(hours=2)
            schedule_review(sender, reservation_datetime)

            # Confirm reservation
            send_message(sender,
                f"✅ Reservation Confirmed!\n\n"
                f"👤 Name: {session['name']}\n"
                f"👥 Party Size: {session['party_size']}\n"
                f"📅 Date: {session['date']}\n"
                f"🕐 Time: {session['time']}\n\n"
                f"We look forward to seeing you at Fork & Flame! 🔥"
            )

            del user_sessions[sender]
            return

    # Default message
    send_message(sender,
        "👋 Welcome to Fork & Flame! 🔥\n\n"
        "How can I help you today?\n\n"
        "📌 *Book a table* — type 'reserve'\n"
        "🕐 *Our hours* — type 'hours'\n"
        "📍 *Location* — type 'location'\n"
        "🍽️ *Menu* — type 'menu'\n"
        "🥗 *Vegetarian options* — type 'vegetarian'\n"
        "🚗 *Parking* — type 'parking'\n"
        "📶 *WiFi* — type 'wifi'"
    )