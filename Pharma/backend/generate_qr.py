import qrcode
import os
from config import QR_FOLDER, BASE_URL

def generate_qr(batch_no):
    """Generates a QR code for a given batch number."""
    qr_data = f"{BASE_URL}{batch_no}"
    qr = qrcode.make(qr_data)
    qr_path = os.path.join(QR_FOLDER, f"{batch_no}.png")
    qr.save(qr_path)
    return qr_path
