import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def save_reservation(name, phone, party_size, date, time):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope
        )
        client = gspread.authorize(creds)
        sheet = client.open("Restaurant Reservations").sheet1

        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            name,
            phone,
            party_size,
            date,
            time
        ])
        print(f"Reservation saved for {name}")
    except Exception as e:
        print(f"Sheets error: {e}")