import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('vader_lexicon', quiet=True)
 # ← text здесь не задан

sia = SentimentIntensityAnalyzer()

def analyze_individual(text):
    
    from ai_analysis import analyze_with_ai
    pluses, minuses = analyze_with_ai(text)
    sentiment = 0  # если нужно добавить что-то ещё

    text = text.lower()
    pluses = []
    minuses = []

    sentiment = sia.polarity_scores(text)["compound"]
    if sentiment > 0.3:
        pluses.append("Позитивный настрой")
    elif sentiment < -0.3:
        minuses.append("Негативный/пессимистичный тон")

    if any(w in text for w in ["ответствен", "внимател", "организован"]):
        pluses.append("Ответственный/внимательный")
    if any(w in text for w in ["путаю", "нервничаю", "конфликт"]):
        minuses.append("Потенциальные трудности в общении")

    return pluses, minuses, sentiment

def analyze_multiple(texts):
    pluses_all = []
    minuses_all = []
    sentiments = []
    result = ""

    for i, text in enumerate(texts):
        pluses, minuses, sentiment = analyze_individual(text)
        pluses_all.append(pluses)
        minuses_all.append(minuses)
        sentiments.append(sentiment)
        result += f"Сотрудник {i+1}:\n  ➕ " + "; ".join(pluses or ["-"]) + "\n  ➖ " + "; ".join(minuses or ["-"]) + f"\n  Тональность: {sentiment:.2f}\n\n"

    # Оценка шанса успеха
    avg_sent = sum(sentiments) / len(sentiments)
    success_chance = min(max((avg_sent + 1) / 2, 0), 1) * 100
    result += f"\n🧠 Оценка шанса успеха выполнения задачи: {success_chance:.1f}%"

    return result.strip(), sentiments

