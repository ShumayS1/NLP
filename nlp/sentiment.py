
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon", quiet=True)

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> float:
    if not text.strip():
        return 0.0
    score = analyzer.polarity_scores(text)
    return score["compound"]
