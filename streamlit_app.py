import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page config for a mobile-friendly look
st.set_page_config(page_title="Site Measure Pro", layout="centered")

# Establish Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📐 Site Measurement Form")

with st.form("measurement_form"):
    # Header: Bold Customer Info
    st.subheader("Customer Details")
    cust_name = st.text_input("Customer Name")
    address = st.text_area("Site Address")
    
    st.divider()
    
    # Measurements Section
    st.subheader("Room Specifications")
    col1, col2 = st.columns(2)
    with col1:
        ceil_ht = st.text_input("Ceiling Height")
        run_len = st.text_input("Overall Length of Run")
    with col2:
        room_dims = st.text_input("Room Dimensions (LxW)")
        fireplace = st.selectbox("Fireplace?", ["No", "Yes"])

    # Cabinetry Details
    st.subheader("Design Preferences")
    appliances = st.text_area("Appliance List (Make/Model/Dims)")
    style = st.text_input("Cabinet Style")
    color = st.text_input("Cabinet Color/Finish")

    # The Submission Button
    submit_button = st.form_submit_button(label="Finalize & Save Project")

    if submit_button:
        if not cust_name or not address:
            st.error("Please enter at least the Name and Address.")
        else:
            # Create a dataframe for the new entry
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Customer Name": cust_name,
                "Address": address,
                "Ceiling Height": ceil_ht,
                "Run Length": run_len,
                "Room Dimensions": room_dims,
                "Fireplace": fireplace,
                "Appliances": appliances,
                "Style": style,
                "Color": color
            }])
            
            # Append to existing sheet
            existing_data = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.success(f"Successfully logged project: {cust_name}")
            st.balloons()
