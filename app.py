import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Our Google Drive search tool
def search_drive(query: str) -> str:
    """
    Searches the designated Google Drive folder for files matching the query in their names.
    """
    print(f"\n[SYSTEM]: AI called 'search_drive' with search query: '{query}'")
    
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    if credentials_json:
        # Load credentials directly from the environment variable string
        info = json.loads(credentials_json)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES
        )
    else:
        # Fall back to the local file (Local Mode)
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



# A) Set a professional page title and subheader
st.title("🤖 DriveChatBot")
st.caption("Stateful Conversational AI Agent for Google Drive File Discovery")

# B) Build a premium Recruiter Sidebar Guide!
with st.sidebar:
    st.title("💼 Recruiter Welcome Hub")
    st.markdown("""
    Welcome! This Conversational AI Agent was engineered by **Harkirat Singh** to demonstrate production-grade Python backend development, API integration, and AI tool calling.
    
    ### 🔍 Live Test Prompts:
    *Copy and paste these exact queries into the chat box to test the AI's capabilities live!*
    
    1. **Find real folders:**
       * *"Do I have a folder named 'pics'?"*
    2. **Find real documents:**
       * *"Find my Daily Report files."*
    3. **Get direct links:**
       * *"Find the bounceup folder and give me a clickable link to open it."*
    4. **Test AI memory:**
       * Ask: *"Do I have any files about invoices?"*
       * Then ask: *"What was the ID of that folder again?"* (Gemini will remember the previous context!).
       
    ---
    
    ### 🛠️ Architecture Highlights:
    * **Google Gemini 2.5 Flash** (Modern `google-genai` SDK)
    * **Google Drive API v3** (OAuth 2.0 Service Account credentials)
    * **Dynamic Tool Calling / Function Calling** (ReAct agent pattern)
    * **Stateful Chat Session Memory** (`st.session_state` persistence)
    * **DevOps Best Practices** (Platform-agnostic dependencies & secure fallback configuration)
    
    🔗 **[View Source Code on GitHub](https://github.com/kirat884/DriveChatBot-)**
    """)

# 1. Initialize chat history in session state
# 1. Initialize chat history and stateful AI session in our vault
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
if "chat" not in st.session_state:
    # We create the chat session ONCE and register our Drive tool inside it!
    st.session_state["chat"] = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [search_drive]
        }
    )
# 2. Display all our past chat messages in beautiful chat bubbles
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. Get user input from the chat input box
user_input = st.chat_input("Ask about your Google Drive files...")

# 4. If the user types a message and hits enter:
if user_input:
    # A) Display the user's message in a chat bubble immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # B) Save the user's message to our session history list
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # C) Send the message to our stateful AI session in memory
    # Gemini will automatically choose to call 'search_drive' if needed!
    response = st.session_state["chat"].send_message(user_input)
    
    # D) Display the AI's response in a chat bubble
    with st.chat_message("assistant"):
        st.write(response.text)
        
    # E) Save the AI's response to our session history list
    st.session_state["messages"].append({"role": "assistant", "content": response.text})