import streamlit as st
import gspread
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
FOLDER_ID="1T3RiNpcYS-vbtSa_AN7z_ZlQbiZtLJfj"

# Function to write data to Google Sheet
def append_to_google_sheet(name, email,events,link):

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)
    client = gspread.authorize(creds)

    # Replace 'Sheet Name' with your actual+ sheet name
    sheet = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw").worksheet("Sheet1")
    sheet.find()

st.write("Hello World")
st.info('This is a purely informational message', icon="ℹ️")