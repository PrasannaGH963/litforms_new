import streamlit as st
import gspread
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pandas as pd
from gspread_dataframe import set_with_dataframe
FOLDER_ID="1T3RiNpcYS-vbtSa_AN7z_ZlQbiZtLJfj"

# Function to write data to Google Sheet


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)
client = gspread.authorize(creds)

# Replace 'Sheet Name' with your actual+ sheet name
sheet = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw").worksheet("Sheet1")


st.title("Team Registration")
st.info('Fill this form only after you have completed registration', icon="ℹ️")
search_id = st.text_input("Enter your ID:")


student_data = None
if search_id:
    # Search for the ID in the Google Sheet
    cell = sheet.find(search_id)
    if cell:
        # Get the corresponding events for the found ID
        name_str = sheet.cell(cell.row, cell.col - 9).value
        st.write(f"Hallo, {name_str} 👋!")
        events_str = sheet.cell(cell.row, cell.col - 2).value
        events_list = events_str.split(',') if events_str else []

        st.write(f"Events for ID {search_id}:")
        st.write(events_list)

        # Store student details including event and teammate information in a dictionary
        student_data = {
            'ID': search_id,
            'Events': events_str,
            'Teammates': []
        }

        for event in events_list:
            st.write(f"Teammates for Event: {event}")
            num_teammates = st.number_input(f"Number of teammates for Event {event}:", min_value=0, max_value=5, step=1)
            if num_teammates > 0:
                teammates_info = []
                for i in range(num_teammates):
                    teammate_name = st.text_input(f"Teammate {i + 1} Name for Event {event}:")
                    teammate_number = st.text_input(f"Teammate {i + 1} Number for Event {event}:")
                    teammate_email = st.text_input(f"Teammate {i + 1} Email for Event {event}:")
                    teammates_info.append({
                        'Name': teammate_name,
                        'Number': teammate_number,
                        'Email': teammate_email
                    })

                student_data['Teammates'].append({event: teammates_info})

# Once all data is collected, write to the Google Sheet
if student_data:
    df = pd.DataFrame(student_data)
    c = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw")
    sheet2 = c.worksheet("test")
    # row_to_update = cell1.row  # Update the same row where the ID was found
    # col_to_update = cell1.col   # Assuming details start from column C

    # Clear existing data and write the new DataFrame to the Google Sheet
    # sheet2.update(f'C{row_to_update}', [[]])  # Clear existing data
    if st.button("Submit"):
        set_with_dataframe(sheet2, df, include_index=True, include_column_header=True)
        st.success("Team Registered")
elif not student_data:
    st.warning("Please fill all the fields")

    # st.write("Data successfully updated in Google Sheet.")
elif search_id:
    st.write("ID not found.")

