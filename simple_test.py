import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("="*50)
print("TESTING GEMINI API")
print("="*50)

# Use POST request (not GET) for generateContent
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

data = {
    "contents": [{
        "parts": [{"text": "Say 'AI is working!'"}]
    }]
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"✅ SUCCESS!")
    print(f"Response: {result['candidates'][0]['content']['parts'][0]['text']}")
else:
    print(f"❌ Error: {response.text}")