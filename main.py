import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Function to write data to Google Sheet
def append_to_google_sheet(name, email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)
    client = gspread.authorize(creds)

    # Replace 'Sheet Name' with your actual sheet name
    sheet = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw").worksheet("Sheet1")
    sheet.append_row([name, email])
    st.success("Data written to Google Sheet successfully!")


# Streamlit form
st.title("Form to Google Sheet")
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
uploaded_file = st.file_uploader("Choose a file")

if st.button("Submit"):
    if name and email:
        append_to_google_sheet(name, email)
    else:
        st.warning("Please fill in both fields.")
