from flask import Flask, request
from bot import handle_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    sender = data.get("from", "")
    message = data.get("body", "").strip().lower()
    
    if sender and message:
        handle_message(sender, message)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)