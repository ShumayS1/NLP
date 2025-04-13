
import nltk
from nlp.sentiment import analyze_sentiment
from ai_analysis import analyze_with_ai
from nlp.text_features import compute_similarity_matrix
nltk.download("punkt", quiet=True)

def analyze_individual(text):
    pluses, minuses = analyze_with_ai(text)
    sentiment = analyze_sentiment(text)
    return pluses, minuses, sentiment

def analyze_multiple(texts):
    individual_results = []
    for text in texts:
        pluses, minuses, sentiment = analyze_individual(text)
        individual_results.append({
            "pluses": pluses,
            "minuses": minuses,
            "sentiment": sentiment
        })

    compatibility_scores = []
    sim_matrix = compute_similarity_matrix(texts)
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            score = sim_matrix[i][j] * 100
            compatibility_scores.append(((i, j), score))

    return individual_results, compatibility_scores
