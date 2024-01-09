import streamlit as st
import gspread
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

FOLDER_ID = "1T3RiNpcYS-vbtSa_AN7z_ZlQbiZtLJfj"

#function to add header image
def add_image_header(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        st.image(image_data)

add_image_header("headerbgps.png")



# Function to write data to Google Sheet


def append_to_google_sheet(name, email, college, year, department, contact_no, alternate_contact_no, events, link):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)
    client = gspread.authorize(creds)

    # Replace 'Sheet Name' with your actual sheet name
    sheet = client.open_by_key("1VeWt6NBUGqc_4TldxqFfrw9qWhd_4n_FKM0H0XEvoLw").worksheet("Sheet1")
    sheet.append_row([name, email, college, year, department, contact_no, alternate_contact_no, events, link])
    st.success("Event Registration completed successfully!")


# Path to your credentials JSON file
CREDENTIALS_FILE = 'litforms.json'  # Replace with your credentials file path

# Function to upload file to Google Drive

def file_exists(service, file_name):
    results = service.files().list(q=f"name='{file_name}'").execute()
    items = results.get('files', [])
    return len(items) > 1


def upload_to_drive(file_path, file_name, mime_type, folder_id):
    scope = ['https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive.metadata'
             ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("litforms.json", scope)

    # Authorize the API client
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,  # Use the provided file name for the uploaded file
        "parents": [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)

    # Upload the file to Drive
    if not file_exists(service, file_name):
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        st.write(f'File uploaded successfully')
        return file.get('id')
    else:
        st.warning('A document with this name already exists!')
        return "extra"


# Streamlit app
st.title("ACUNETIX 11.0 Registration")

# User input fields
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")

# College selection
college_option = ["Dr. D. Y. Patil Institute Of Technology", "Other"]
college = st.selectbox("Select your college", college_option)

# If 'Other' is selected, display additional text input
if college == "Other":
    college = st.text_input("Enter your college name (if other)")

year_options = ["FE", "SE", "TE", "BE"]
year = st.selectbox("Select your year", year_options,placeholder="Enter your year")
department_options = ['Artificial Intelligence & Data Science', 'Automation & Robotics', 'Civil', 'Computer', 'Electrical',
                      'Electronics & Telecommunication', 'Information Technology', 'Instrumentation', 'Mechanical']

department = st.selectbox("Enter your department", department_options,placeholder="Enter your Branch")
contact_no = st.text_input("Enter your contact number", max_chars=10, min_char=10)
alternate_contact_no = st.text_input("Enter your alternate contact number", max_chars=10)

# Checkbox for events
st.title("Events in ACUNETIX 11.0")
costs = {
    'Innovatia': 10,
    'DPL': 20,
    'Code of Lies': 30,
    'Ctrl-Alt-Elite': 40,
    'MUN': 50,
    'Brainiac': 60,
    'Gamestorm': 70,
    'Treasure Trove': 80,
    'PromptAI': 90,
    '11hr Hackathon': 100
}

selected_items = {}
for label, cost in costs.items():
    checkbox_state = st.checkbox(label)
    if checkbox_state:
        selected_items[label] = cost

total_cost = sum(selected_items.values())
events = ",".join(list(selected_items.keys()))

# Display the total cost and payment button
st.write(f"Total Cost: {total_cost}")
redirect_url = f"upi://pay?pa=pranavmehe14@okicici&pn=Pranav&cu=INR&am={total_cost}"

# button_styles = """
#     <style>
#         .custom-link {
#             display: inline-block;
#             padding: 8px 16px;
#             text-align: center;
#             text-decoration: none;
#             color: black;
#             background-color: white;
#             border: 1px solid #D3D3D3;
#             border-radius: 8px;
#             transition: background-color 0.3s, color 0.3s;
#         }
#         .custom-link:hover {
#             background-color: light-red;
#             color: red;
#             border: 1px solid red;
#         }
#     </style>
# """
# st.components.v1.html(
#     button_styles +
#     f'<a href="{redirect_url}" class="custom-link" target="_blank">Payment</a>'
# )
st.link_button("Payment", redirect_url)
# File upload section
st.title('File Upload to Google Drive')
uploaded_file = st.file_uploader("Upload a file", type=['jpg', 'png', 'pdf'])

if uploaded_file is not None:
    with open('temp_file', 'wb') as temp_file:
        temp_file.write(uploaded_file.getvalue())

    file_extension = uploaded_file.name.split('.')[-1].lower()
    mime_types = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'pdf': 'application/pdf'
    }
    mime_type = mime_types.get(file_extension)

    if mime_type:
        file_id = upload_to_drive('temp_file', uploaded_file.name, mime_type, FOLDER_ID)
        link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

        if file_id != "extra":
            if st.button("Submit"):
                if name and email and college and year and department and contact_no and alternate_contact_no \
                        and events and link:
                    # college_name = college if college != "Other" else other_college
                    append_to_google_sheet(name, email, college, year, department, contact_no,
                                           alternate_contact_no, events, link)
                else:
                    st.warning("Please fill in all fields.")
    else:
        st.write('File type not supported. Please upload JPG, PNG, or PDF files.')