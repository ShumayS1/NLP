
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

sia = SentimentIntensityAnalyzer()

def analyze_texts(text1, text2):
    # Анализ тональности
    score1 = sia.polarity_scores(text1)["compound"]
    score2 = sia.polarity_scores(text2)["compound"]

    sentiment_diff = abs(score1 - score2)

    # TF-IDF сравнение
    vect = TfidfVectorizer()
    tfidf_matrix = vect.fit_transform([text1, text2])
    similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]


    report = f"""
    Совпадение по теме (TF-IDF): {similarity:.2f}
    Различие в эмоциональной окраске: {sentiment_diff:.2f}
    """

    return report.strip()
