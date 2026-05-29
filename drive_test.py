import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
load_dotenv()

folder_id = os.getenv("FOLDER_ID")

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


creds = service_account.Credentials.from_service_account_file(
    "service_account.json", scopes=SCOPES
    )

service = build("drive", "v3", credentials=creds)


query = f"'{folder_id}' in parents and trashed = false"

results = service.files().list(
    q=query,
    fields="files(id, name, mimeType)"
).execute()

files = results.get("files", [])


print("\n--- Files found in Google Drive ---")
if not files:
    print("No files found! Did you share the folder with the service account email?")
else:
    for f in files:
        print(f"Name: {f['name']} | Type: {f['mimeType']} | ID: {f['id']}")