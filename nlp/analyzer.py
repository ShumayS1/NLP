
from nlp.text_features import extract_features
from nlp.sentiment import estimate_sentiment
from ai_analysis import analyze_with_ai
from itertools import combinations

def analyze_individual(text):
    pluses, minuses = analyze_with_ai(text)
    sentiment = estimate_sentiment(text)
    return pluses, minuses, sentiment

def analyze_multiple(texts):
    results = []
    sentiments = []
    for text in texts:
        pluses, minuses, sentiment = analyze_individual(text)
        results.append({"pluses": pluses, "minuses": minuses})
        sentiments.append(sentiment)

    result_text = ""
    for i, res in enumerate(results):
        result_text += f"Сотрудник {i+1}:"
        result_text += f"  👍 Плюсы: {', '.join(res['pluses']) or '—'}\n"
        result_text += f"  👎 Минусы: {', '.join(res['minuses']) or '—'}\n"
        result_text += f"  💬 Тональность: {sentiments[i]:.2f}\n\n"

    compatibility_scores = {}
    for (i, j) in combinations(range(len(texts)), 2):
        score = 100 - abs(sentiments[i] - sentiments[j]) * 100
        key = f"Сотрудник {i+1} и Сотрудник {j+1}"
        compatibility_scores[key] = max(0, min(score, 100))

    return result_text, compatibility_scores
