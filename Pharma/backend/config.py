import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.db")
QR_FOLDER = os.path.join(BASE_DIR, "qr_codes")
IMAGE_FOLDER = os.path.join(BASE_DIR, "static/tablet_images")
BASE_URL = "http://127.0.0.1:5000/tablet/"

# Ensure directories exist
os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
