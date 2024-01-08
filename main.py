import streamlit as st
import gspread
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json


with open("config.json", "r") as file:
    parameters = json.load(file)['params']

FOLDER_ID= parameters['FOLDER_ID']


# Function to write data to Google Sheet
def append_to_google_sheet(name, email,events,link):
    scope = ['https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata'
  ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(parameters['CREDS_FILE'], scope)
    client = gspread.authorize(creds)

    # Replace 'Sheet Name' with your actual+ sheet name
    sheet = client.open_by_key(parameters['G_SHEET_ID']).worksheet(parameters['SHEET_NAME'])
    sheet.append_row([name, email,events,link])
    st.success("Event Registration completed successfully!")

# Function to upload file to Google Drive
def upload_to_drive(file_path, file_name, mime_type,folder_id):
    # Load credentials from the credentials file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(parameters['CREDS_FILE'], scope)

    # Authorize the API client
    service = build('drive', 'v3', credentials=creds)
    # try:
    # # folder = service.files().get(fileId=folder_id, fields='id, mimeType').execute()
    # service.files()
    # if folder.get('mimeType') == 'application/vnd.google-apps.folder':
    file_metadata = {
        'name': file_name,  # Use the provided file name for the uploaded file
        "parents": [folder_id]

    }
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    # Upload the file to Drive
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file.get('id')
        # The ID represents a folder
      # The ID does not represent a folder
    # except HttpError as e:
    #     if e.resp.status == 404:
    #         st.write("Error in uploading file1234")  # Folder not found (or permission issue)
    #     else:
    #         raise  # Other HTTP error occurred

    # Define file metadata and upload

# Streamlit app


# Streamlit form
st.title("ACUNETIX 11.0 Registration")
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
# uploaded_file = st.file_uploader("Choose a file")


# Empty dictionary to store the selected checkboxes and their costs
selected_items = {}

# Display checkboxes and calculate total cost
st.title("Events in ACUNETIX 11.0")

# Iterate through the dictionary to create checkboxes
for label, cost in parameters['events'].items():
    checkbox_state = st.checkbox(label)
    if checkbox_state:
        selected_items[label] = cost

# Calculate total cost based on selected checkboxes
total_cost = sum(selected_items.values())
events = ",".join(list(selected_items.keys()))
# Display the total cost
# st.write(f"Total Cost: {total_cost}")

Rid = "AAAA0000"                                      #TODO:Fetch Ids from google sheet

redirect_url = f"upi://pay?pa={parameters['UPI_ID']}&pn={parameters['pn']}&cu=INR&am={total_cost}&tn={parameters['tn']+str(Rid)}"
# Create the button-like link with specified styles
button_styles = """
    <style>
        /* Default link styles */
        .custom-link {
            display: inline-block;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            color: black;
            background-color: white;
            border: 1px solid #D3D3D3;
            border-radius: 8px;
            transition: background-color 0.3s, color 0.3s;
        }
        /* Link styles on hover */
        .custom-link:hover {
            background-color: light-red;
            color: red;
            border: 1px solid red
        }
    </style>
"""
st.components.v1.html(
    button_styles +
    f'<a href="{redirect_url}" class="custom-link" target="_blank">Payment</a>'
)

st.title('File Upload to Google Drive')

uploaded_file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf'])  # Accept JPG, PNG, and PDF files

if uploaded_file is not None:
    # st.write('File uploaded successfully!')

    # Save the uploaded file to a temporary location
    with open('temp_file', 'wb') as temp_file:
        temp_file.write(uploaded_file.getvalue())

    # Determine the file type based on the uploaded file's extension
    file_extension = uploaded_file.name.split('.')[-1].lower()

    # Define MIME types based on file extensions
    mime_types = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'pdf': 'application/pdf'
    }

    # Get MIME type based on the file extension
    mime_type = mime_types.get(file_extension)

    # Upload the file to Google Drive
    if mime_type:
        file_id = upload_to_drive('temp_file', uploaded_file.name, mime_type,FOLDER_ID)
        st.write(f'File uploaded successfully ')
        link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        # st.markdown(f"[Link](https://drive.google.com/file/d/{file_id}/view?usp=sharing)")
        if st.button("Submit"):
            if name and email and events:
                append_to_google_sheet(name, email, events,link)
            else:
                st.warning("Please fill in all fields.")

    else:
        st.write('File type not supported. Please upload JPG, PNG, or PDF files.')


# if st.button("Go to Example Website"):
#     # st.write(f'<script>window.location.href="https://www.premierleague.com/";</script>', unsafe_allow_html=True)
#     st.components.v1.html(f'<button><a href="https://www.premierleague.com/" target="_blank">Click here to visit the example website</a></button>')




