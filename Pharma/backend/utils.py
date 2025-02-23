import qrcode
import os
import uuid

# Directory to save QR codes
OUTPUT_DIR = "tablet_qr_codes"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Function to generate a random URL
def generate_random_url():
    unique_id = uuid.uuid4()
    return f"https://example.com/tablet/{unique_id}"

# Function to generate QR code for a tablet
def generate_qr_code(tablet):
    tablet_id = tablet["id"]
    tablet_name = tablet["name"]
    unique_url = generate_random_url()
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(unique_url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    # Save QR code image
    image_path = os.path.join(OUTPUT_DIR, f"{tablet_id}_{tablet_name}.png")
    img.save(image_path)

    return image_path, unique_url
