
from nltk.sentiment import SentimentIntensityAnalyzer

def estimate_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    return score["compound"]
