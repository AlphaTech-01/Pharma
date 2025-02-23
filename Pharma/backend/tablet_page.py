import streamlit as st
import urllib.parse

# Tablet database (simulating a real database)
tablets = {
    "TAB001": "Tablet A",
    "TAB002": "Tablet B",
    "TAB003": "Tablet C",
}

# Extract tablet ID from URL
query_params = st.query_params
tablet_id = query_params.get("tablet_id", None)

st.title("📱 Tablet Details Page")

if tablet_id and tablet_id in tablets:
    st.success(f"🔹 You scanned QR for: **{tablets[tablet_id]}**")
    st.write("📌 Here are some details about this tablet:")
    st.write("- **Model:** 2024 Pro Edition")
    st.write("- **Processor:** Snapdragon 8 Gen 2")
    st.write("- **Display:** 11-inch OLED")
    st.write("- **Battery:** 10,000mAh")
else:
    st.error("❌ Invalid Tablet QR Code")
