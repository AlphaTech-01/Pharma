import streamlit as st
import sqlite3
import os
import qrcode
from PIL import Image
from datetime import datetime, timedelta
from database import get_db_connection, create_tables  # Import database functions

# Initialize the database
create_tables()

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_CODE_DIR = os.path.join(BASE_DIR, "static", "qr_codes")
TABLET_IMG_DIR = os.path.join(BASE_DIR, "static", "tablet_images")

# Ensure directories exist
os.makedirs(QR_CODE_DIR, exist_ok=True)
os.makedirs(TABLET_IMG_DIR, exist_ok=True)

# Function to generate QR Code
def generate_qr_code(batch_no):
    qr = qrcode.make(batch_no)  # QR will contain just batch_no
    qr_path = os.path.join(QR_CODE_DIR, f"{batch_no}.png")
    qr.save(qr_path)
    return qr_path

# Function to fetch tablet details by batch_no
def fetch_tablet_by_batch(batch_no):
    conn = get_db_connection()
    tablet = conn.execute("SELECT * FROM tablets WHERE batch_no = ?", (batch_no,)).fetchone()
    conn.close()
    return tablet

# Streamlit UI
st.set_page_config(page_title="Pharma QR Admin", layout="wide")
st.title("💊 Pharma QR Admin Panel")

# Step 1: Admin adds tablet details
with st.form(key="add_tablet"):
    name = st.text_input("Tablet Name")
    batch_no = st.text_input("Batch Number")
    manufacturing_date = st.date_input("Manufacturing Date")
    shelf_life_days = st.number_input("Shelf Life (days)", min_value=1, max_value=3650)
    description = st.text_area("Description")
    image_file = st.file_uploader("Upload Tablet Image", type=["png", "jpg", "jpeg"])
    
    submit_button = st.form_submit_button("Generate QR Code")

    if submit_button:
        expiry_date = manufacturing_date + timedelta(days=shelf_life_days)
        img_filename = f"{batch_no}.png"

        # Save the image
        if image_file:
            img_path = os.path.join(TABLET_IMG_DIR, img_filename)
            with open(img_path, "wb") as f:
                f.write(image_file.getbuffer())

        # Insert into database
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO tablets (name, batch_no, manufacturing_date, expiry_date, description, image) VALUES (?, ?, ?, ?, ?, ?)",
            (name, batch_no, manufacturing_date.strftime("%Y-%m-%d"), expiry_date.strftime("%Y-%m-%d"), description, img_filename),
        )
        conn.commit()
        conn.close()

        # Generate QR Code
        qr_path = generate_qr_code(batch_no)

        st.success(f"✅ Tablet **{name}** added successfully!")
        st.image(qr_path, caption="Scan this QR Code", width=200)

# Step 2: QR Scanner to fetch details
st.header("🔍 Scan QR Code")

qr_input = st.text_input("Enter Batch No from QR Code")

if st.button("Fetch Tablet Details"):
    tablet = fetch_tablet_by_batch(qr_input)

    if tablet:
        st.subheader(f"📦 {tablet['name']} (Batch: {tablet['batch_no']})")
        st.write(f"🛠 **Manufacturing Date:** {tablet['manufacturing_date']}")
        st.write(f"⏳ **Expiry Date:** {tablet['expiry_date']}")
        st.write(f"📜 **Description:** {tablet['description']}")

        # Display Tablet Image
        img_path = os.path.join(TABLET_IMG_DIR, tablet['image'])
        if os.path.exists(img_path):
            st.image(img_path, caption="Tablet Image", width=200)
    else:
        st.error("❌ No tablet found for this batch number.")
