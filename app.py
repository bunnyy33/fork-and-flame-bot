import os
from flask import Flask, request
from bot import handle_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True) or request.form.to_dict()
    print(f"ALL DATA RECEIVED: {data}")
    
    sender = data.get("from", "")
    message = data.get("body", "").strip().lower()
    print(f"Sender: {sender}")
    print(f"Message: {message}")
    
    if sender and message:
        handle_message(sender, message)
    
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)