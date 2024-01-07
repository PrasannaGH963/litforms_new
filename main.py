import streamlit as st
import gspread
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Function to write data to Google Sheet
def append_to_google_sheet(name, email):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)
    client = gspread.authorize(creds)

    # Replace 'Sheet Name' with your actual+ sheet name
    sheet = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw").worksheet("Sheet1")
    sheet.append_row([name, email])
    st.success("Data written to Google Sheet successfully!")

# Path to your credentials JSON file
CREDENTIALS_FILE = 'litforms.json'  # Replace with your credentials file path


# Function to upload file to Google Drive
def upload_to_drive(file_path, file_name, mime_type,folder_id):
    # Load credentials from the credentials file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)

    # Authorize the API client
    service = build('drive', 'v3', credentials=creds)
    try:
        folder = service.files().get(fileId=folder_id, fields='id, mimeType').execute()

        if folder.get('mimeType') == 'application/vnd.google-apps.folder':
            file_metadata = {
                'name': file_name,  # Use the provided file name for the uploaded file
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_path, mimetype=mime_type)

            # Upload the file to Drive
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            return file.get('id')
            # The ID represents a folder
        else:
            return False  # The ID does not represent a folder
    except HttpError as e:
        if e.resp.status == 404:
            return False  # Folder not found (or permission issue)
        else:
            raise  # Other HTTP error occurred

    # Define file metadata and upload

# Streamlit app


# Streamlit form
st.title("Form to Google Sheet")
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
# uploaded_file = st.file_uploader("Choose a file")

costs = {
    'Checkbox 1': 10,
    'Checkbox 2': 20,
    'Checkbox 3': 30,
    'Checkbox 4': 40,
    'Checkbox 5': 50,
    'Checkbox 6': 60,
    'Checkbox 7': 70,
    'Checkbox 8': 80,
    'Checkbox 9': 90,
    'Checkbox 10': 100
}

# Empty dictionary to store the selected checkboxes and their costs
selected_items = {}

# Display checkboxes and calculate total cost
st.title("Checkbox Example")

# Iterate through the dictionary to create checkboxes
for label, cost in costs.items():
    checkbox_state = st.checkbox(label)
    if checkbox_state:
        selected_items[label] = cost

# Calculate total cost based on selected checkboxes
total_cost = sum(selected_items.values())

# Display the total cost
# st.write(f"Total Cost: {total_cost}")
redirect_url = f"upi://pay?pa=pranavmehe14@okicici&pn=Pranav&cu=INR&am={total_cost}"
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
    f'<a href="{redirect_url}" class="custom-link" target="_blank">Click here to visit the example website</a>'
)

st.title('File Upload to Google Drive')

uploaded_file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf'])  # Accept JPG, PNG, and PDF files

if uploaded_file is not None:
    st.write('File uploaded successfully!')

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
        file_id = upload_to_drive('temp_file', uploaded_file.name, mime_type,folder_id="1T3RiNpcYS-vbtSa_AN7z_ZlQbiZtLJfj")
        st.write(f'File successfully uploaded to Google Drive. File ID: {file_id}')
    else:
        st.write('File type not supported. Please upload JPG, PNG, or PDF files.')

# if st.button("Go to Example Website"):
#     # st.write(f'<script>window.location.href="https://www.premierleague.com/";</script>', unsafe_allow_html=True)
#     st.components.v1.html(f'<button><a href="https://www.premierleague.com/" target="_blank">Click here to visit the example website</a></button>')



if st.button("Submit"):
    if name and email:
        append_to_google_sheet(name, email)
    else:
        st.warning("Please fill in both fields.")
