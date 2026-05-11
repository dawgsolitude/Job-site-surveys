import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Site Measure Pro", layout="centered")

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📐 Site Measurement Form")

with st.form("measurement_form", clear_on_submit=True):
    st.subheader("Customer Details")
    cust_name = st.text_input("Customer Name")
    address = st.text_area("Site Address")
    
    st.divider()
    
    st.subheader("Room Specifications")
    col1, col2 = st.columns(2)
    with col1:
        ceil_ht = st.text_input("Ceiling Height")
        run_len = st.text_input("Overall Length of Cabinet Run")
    with col2:
        room_dims = st.text_input("Overall Dimensions of Room")
        fireplace = st.radio("Fireplace?", ["No", "Yes"])

    st.subheader("Cabinet Details")
    appliances = st.text_area("Appliance List")
    style = st.text_input("Cabinet Style")
    color = st.text_input("Cabinet Color")

    submit_button = st.form_submit_button(label="Finalize & Save Project")

    if submit_button:
        if not cust_name or not address:
            st.error("Please enter Name and Address.")
        else:
            try:
                # Prepare the data
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer Name": cust_name, "Address": address,
                    "Ceiling Height": ceil_ht, "Run Length": run_len,
                    "Room Dimensions": room_dims, "Fireplace": fireplace,
                    "Appliances": appliances, "Style": style, "Color": color
                }])
                
                # Use a safer read/write method
                try:
                    existing_data = conn.read(worksheet="Sheet1")
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                except:
                    # If Sheet1 doesn't exist or is empty, just use the new row
                    updated_df = new_row
                
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success(f"Project for {cust_name} saved!")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
