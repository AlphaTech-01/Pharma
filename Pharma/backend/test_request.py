import sqlite3
import requests

# Connect to database
conn = sqlite3.connect("backend/database.db")
cursor = conn.cursor()

# Fetch latest tablet data
cursor.execute("SELECT name, batch_no, manufacturing_date, expiry_date, description, image FROM tablets ORDER BY id DESC LIMIT 1")
tablet = cursor.fetchone()
conn.close()

# If no data exists, exit
if not tablet:
    print("❌ No tablets found in database. Add a tablet first via /admin.")
    exit()

# Prepare data for API request
data = {
    "name": tablet[0],
    "batch_no": tablet[1],
    "manufacturing_date": tablet[2],
    "shelf_life_days": (int((tablet[3] - tablet[2]).days)),  # Convert expiry date
    "description": tablet[4],
    "image": tablet[5]
}

# Send request to generate QR
response = requests.post("http://127.0.0.1:5000/generate_qr", json=data)
print(response.json())
