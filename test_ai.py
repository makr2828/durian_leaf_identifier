import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("="*50)
print("TESTING GEMINI AI")
print("="*50)
print(f"API Key: {api_key[:20]}..." if api_key else "No API key found")

if not api_key:
    print("❌ Please add GEMINI_API_KEY to your .env file")
    exit()

# Configure
genai.configure(api_key=api_key)

# Test models
models_to_test = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']

for model_name in models_to_test:
    try:
        print(f"\nTesting {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'OK'")
        print(f"✅ SUCCESS! {model_name} is working")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower():
            print(f"❌ QUOTA EXCEEDED for {model_name}")
        elif "404" in error_msg:
            print(f"❌ MODEL NOT FOUND: {model_name}")
        else:
            print(f"❌ {model_name} failed: {error_msg[:100]}")

print("="*50)