from sheets import save_reservation
from datetime import datetime, timedelta

user_sessions = {}

FAQS = {
    "hours": "🕐 Fork & Flame is open:\nMon-Fri: 11AM - 11PM\nSat-Sun: 10AM - 12AM",
    "location": "📍 123 Flame Street, London, UK\nGoogle Maps: https://maps.google.com",
    "menu": (
        "🍽️ *Fork & Flame Menu*\n\n"
        "*🥩 Mains*\n"
        "• Grilled Ribeye Steak — £28\n"
        "• Pan Seared Salmon — £22\n"
        "• Chicken Marsala — £18\n"
        "• Lamb Chops — £26\n\n"
        "*🍝 Pasta & Risotto*\n"
        "• Truffle Mushroom Risotto — £16\n"
        "• Lobster Linguine — £24\n\n"
        "*🍰 Desserts*\n"
        "• Chocolate Lava Cake — £8\n"
        "• Tiramisu — £7\n\n"
        "Type *'vegetarian'* to see our veg menu 🥗"
    ),
    "vegetarian": (
        "🥗 *Fork & Flame Vegetarian Menu*\n\n"
        "*🌿 Starters*\n"
        "• Burrata & Heirloom Tomatoes — £10\n"
        "• Roasted Pepper Soup — £7\n\n"
        "*🍽️ Mains*\n"
        "• Wild Mushroom Risotto — £15\n"
        "• Spinach & Ricotta Ravioli — £14\n"
        "• Grilled Halloumi Stack — £13\n"
        "• Butternut Squash Curry — £13\n\n"
        "*🍰 Desserts*\n"
        "• Vanilla Panna Cotta — £7\n"
        "• Berry Cheesecake — £8\n\n"
        "All vegetarian dishes are freshly prepared daily 🌱"
    ),
    "parking": "🚗 Free parking available behind the restaurant.",
    "wifi": "📶 Free WiFi available. Password given at the table."
}

async def handle_message(user_id, message):
    # FAQ checks
    if any(word in message for word in ["hour", "open", "timing"]):
        return FAQS["hours"]

    if any(word in message for word in ["location", "address", "where"]):
        return FAQS["location"]

    if any(word in message for word in ["menu", "food", "dish"]):
        return FAQS["menu"]

    if any(word in message for word in ["vegetarian", "vegan"]):
        return FAQS["vegetarian"]

    if any(word in message for word in ["parking", "park"]):
        return FAQS["parking"]

    if any(word in message for word in ["wifi", "internet"]):
        return FAQS["wifi"]

    # Reservation flow
    if any(word in message for word in ["book", "reserve", "reservation", "table"]):
        user_sessions[user_id] = {"step": "party_size"}
        return (
            "🍽️ Let's get your table reserved at Fork & Flame!\n\n"
            "How many people will be dining?"
        )

    # Handle reservation steps
    if user_id in user_sessions:
        session = user_sessions[user_id]

        if session["step"] == "party_size":
            session["party_size"] = message
            session["step"] = "date"
            return "📅 What date would you like? (e.g. 25 June 2026)"

        if session["step"] == "date":
            session["date"] = message
            session["step"] = "time"
            return "🕐 What time would you like? (e.g. 7:30 PM)"

        if session["step"] == "time":
            session["time"] = message
            session["step"] = "name"
            return "👤 What name should we put the reservation under?"

        if session["step"] == "name":
            session["name"] = message

            save_reservation(
                session["name"],
                user_id,
                session["party_size"],
                session["date"],
                session["time"]
            )

            confirmation = (
                f"✅ *Reservation Confirmed!*\n\n"
                f"👤 Name: {session['name']}\n"
                f"👥 Party Size: {session['party_size']}\n"
                f"📅 Date: {session['date']}\n"
                f"🕐 Time: {session['time']}\n\n"
                f"We look forward to seeing you at Fork & Flame! 🔥"
            )

            del user_sessions[user_id]
            return confirmation

    # Default message
    return (
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
