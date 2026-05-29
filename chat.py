import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

chat = client.chats.create(model="gemini-2.5-flash")
response1= chat.send_message("hello i am kirat")
print(response1.text)

response2 = chat.send_message("what's my name")
print(response2.text)