"""
Durian Leaf Identifier - Using Gemini 2.5 Flash
"""

import google.generativeai as genai
from django.conf import settings
from PIL import Image

def analyze_leaf_image(image_path):
    """Analyze durian leaf image using Gemini AI"""

    try:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return {
                'variety': 'Unknown',
                'confidence': 0,
                'features': 'API key not configured',
                'error': True
            }

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Open image
        image = Image.open(image_path)

        # Use gemini-2.5-flash (available from your test)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = """You are a durian leaf expert. Analyze this leaf and identify which variety it is from: D101, Arancillo, or Puyat.

Return EXACTLY in this format:

VARIETY: [D101 or Arancillo or Puyat]
CONFIDENCE: [0-100]
FEATURES: [Describe shape, color, texture, venation]

Characteristics:
- D101: Light green, oval shape, flat texture, visible flat veins
- Arancillo: Dark green, long/narrow shape, prominent raised veins
- Puyat: Very dark green, broad shape, glossy surface, yellowish midrib"""

        response = model.generate_content([prompt, image])
        response_text = response.text

        # Parse response
        result = {
            'variety': 'Unknown',
            'confidence': 70,
            'features': response_text,
            'error': False
        }

        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('VARIETY:'):
                variety = line.replace('VARIETY:', '').strip()
                if 'D101' in variety:
                    result['variety'] = 'D101'
                elif 'Arancillo' in variety:
                    result['variety'] = 'Arancillo'
                elif 'Puyat' in variety:
                    result['variety'] = 'Puyat'
            elif line.startswith('CONFIDENCE:'):
                try:
                    result['confidence'] = int(line.replace('CONFIDENCE:', '').strip())
                except:
                    pass

        return result

    except Exception as e:
        return {
            'variety': 'Unknown',
            'confidence': 0,
            'features': f'Error: {str(e)}',
            'error': True
        }