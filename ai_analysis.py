import pickle

# Обязательно: Бинарный режим чтения!
def analyze_with_ai(text):
    plus_keywords = [
        "ответственный", "инициативный", "организованный", "аналитичный", "коммуникабельный",
        "умеет слушать", "работает в команде", "внимательный", "стрессоустойчивый", "пунктуальный"
    ]
    minus_keywords = [
        "нервничаю", "откладываю", "иногда теряюсь", "конфликтую", "медлю",
        "злюсь", "устаю быстро", "переживаю", "неуверенность", "раздражаюсь"
    ]

    text_lower = text.lower()
    pluses = [kw for kw in plus_keywords if kw in text_lower]
    minuses = [kw for kw in minus_keywords if kw in text_lower]
    return pluses, minuses

