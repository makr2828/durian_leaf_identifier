import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("="*60)
print("DIAGNOSING API KEY STATUS")
print("="*60)
print(f"API Key: {api_key[:20]}...")

# Test with different endpoints
urls = [
    f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
]

for url in urls:
    print(f"\nTesting: {url[:80]}...")
    response = requests.get(url if "models?" in url else None,
                           json={"contents": [{"parts":[{"text":"Hi"}]}]} if "generateContent" in url else None,
                           headers={"Content-Type": "application/json"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")