import os
from dotenv import load_dotenv
from google import genai
from google.oauth2 import service_account
from googleapiclient.discovery import build


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def search_drive(query: str) -> str:
    """
    Searches the designated Google Drive folder for files matching the query in their names.
    """
    print(f"\n[SYSTEM]: AI called 'search_drive' with search query: '{query}'")
    
    
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = service_account.Credentials.from_service_account_file(
        "service_account.json", scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    
    
    folder_id = os.getenv("FOLDER_ID")
    
   
    drive_query = f"'{folder_id}' in parents and name contains '{query}' and trashed = false"
    
    
    results = service.files().list(
        q=drive_query,
        fields="files(id, name, webViewLink)"
    ).execute()
    
    files = results.get("files", [])
    
    
    return f"Search results from Google Drive: {files}"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Do I have any files about bounceup in my drive?", 
    config={
        "tools": [search_drive] 
    }
)


print("\n[AI Response]:")
print(response.text)