import google.generativeai as genai
from django.conf import settings


def get_chatbot_response(user_message):
    """Get AI response for durian leaf questions"""

    print(f"\n{'=' * 50}")
    print(f"CHATBOT: {user_message}")
    print(f"{'=' * 50}")

    try:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return "⚠️ API key not configured"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""Answer briefly about D101, Arancillo, or Puyat durian leaves: {user_message}"""

        response = model.generate_content(prompt)
        result = response.text

        print(f"AI: {result[:100]}")
        return result

    except Exception as e:
        print(f"ERROR: {e}")
        # Fallback responses
        msg = user_message.lower()
        if "d101" in msg:
            return "🌿 D101 leaves are light green with an oval to oblong shape. They have a flat texture with visible flat veins."
        elif "arancillo" in msg:
            return "🌿 Arancillo leaves are dark green, long and narrow, with prominent raised veins."
        elif "puyat" in msg:
            return "🌿 Puyat leaves are very dark green, broad in shape, with a glossy surface and yellowish midrib."
        else:
            return "🌿 I can help identify D101, Arancillo, and Puyat leaves! Ask me about specific varieties."