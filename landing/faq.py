FAQ_DATA = {
    "what is durian leaf identifier": "Durian Leaf Identifier is an AI-powered tool that identifies durian varieties by analyzing photos of their leaves. Different durian varieties have unique leaf characteristics.",

    "how to identify durian by leaves": "Durian leaves can be identified by: 1) Leaf shape (oblong, elliptic, lanceolate), 2) Leaf apex (pointed, rounded), 3) Venation pattern, 4) Leaf margin, 5) Color and texture.",

    "musang king leaf characteristics": "Musang King leaves are oblong-elliptic in shape, dark green, leathery texture, prominent pinnate venation, rounded base, and pointed apex.",

    "monthong leaf features": "Monthong leaves are larger (15-20cm), lighter green, thinner texture, more elongated shape, and slightly wavy margin.",

    "d24 leaf identification": "D24 leaves are medium size (12-16cm), dark green with glossy surface, thick and leathery, with prominent yellowish midrib.",

    "how to use leaf identifier": "1) Login to your account, 2) Click 'Identify Leaf' in the menu, 3) Upload a clear photo of a durian leaf, 4) Our AI will analyze and identify the variety, 5) View results with confidence score.",

    "best way to photograph leaves": "Tips: 1) Use natural daylight, 2) Place on plain background, 3) Take top-down photo, 4) Include mature leaves, 5) Avoid shadows, 6) Ensure clear focus.",
}


def get_faq_answer(question):
    question_lower = question.lower().strip()

    # Direct match
    if question_lower in FAQ_DATA:
        return FAQ_DATA[question_lower]

    # Keyword matching
    keywords = {
        'musang king': 'musang king leaf characteristics',
        'musang': 'musang king leaf characteristics',
        'monthong': 'monthong leaf features',
        'd24': 'd24 leaf identification',
        'identify leaf': 'how to use leaf identifier',
        'upload photo': 'how to use leaf identifier',
        'photograph': 'best way to photograph leaves',
    }

    for key, answer_key in keywords.items():
        if key in question_lower:
            return FAQ_DATA.get(answer_key, "Check our documentation for leaf identification tips!")

    return None