import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/skillbridgebot-cred.json', scope)
    client = gspread.authorize(creds)
    return client

# Get or create a workbook
def get_or_create_course_workbook(course_name, is_scholarship=False):
    client = authenticate_google_sheets()
    sheet_type = "scholarship" if is_scholarship else "registration"
    
    try:
        workbook = client.open(f"{course_name}_{sheet_type}")
        worksheet = workbook.sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        workbook = client.create(f"{course_name}_{sheet_type}")
        worksheet = workbook.get_worksheet(0)
        set_up_columns(worksheet, sheet_type)

    return workbook, worksheet

# Set column headers for registration or scholarship
def set_up_columns(worksheet, sheet_type):
    if sheet_type == "registration":
        columns = ["Student ID", "Name", "Phone", "Email", "Registration Time", "Address",
                   "Course Name", "Highest Education Level", "Institution", "Source", "More Info", "Status"]
    else:  # For scholarship
        columns = ["Student ID", "Name", "Phone", "Email", "Scholarship Time", "Address",
                   "Course Name", "Why You Deserve", "Scholarship Status"]
    worksheet.insert_row(columns, 1)

# Add student data to Google Sheets
def add_student_to_course(course_name, student_data, is_scholarship=False):
    workbook, worksheet = get_or_create_course_workbook(course_name, is_scholarship)
    worksheet.append_row(student_data)
