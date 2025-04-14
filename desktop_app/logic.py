# logic.py
import pandas as pd
import numpy as np
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
if not os.path.exists("assets"):
    os.makedirs("assets")

wordcloud_path = os.path.join("assets", "wordcloud.png")
heatmap_path = os.path.join("assets", "heatmap.png")
nltk.download('stopwords')
stop_words = set(stopwords.words("russian"))
stemmer = RussianStemmer()

model = joblib.load("success_predictor.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def preprocess(text):
    text = re.sub(r"[^\w\s]", "", str(text).lower())
    tokens = text.split()
    return " ".join([stemmer.stem(w) for w in tokens if w not in stop_words])

def run_local_analysis(csv_path):
    df = pd.read_csv(csv_path)
    df['cleaned'] = df['Текст_отзыва'].apply(preprocess)

    X = vectorizer.transform(df['cleaned'])
    probs = model.predict_proba(X)[:, 1]
    success_rate = float(np.mean(probs))

    positive_words = ["нрав", "команд", "слаж", "удоб"]
    negative_words = ["конфликт", "давлен", "перегруз", "недостат"]

    positives = []
    negatives = []
    for text in df['cleaned']:
        if any(word in text for word in positive_words):
            positives.append("Обнаружены позитивные отзывы")
        if any(word in text for word in negative_words):
            negatives.append("Есть жалобы или конфликты")

    sim_matrix = cosine_similarity(X)
    names = df['Имя'].tolist()
    pair_scores = {}
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            key = f"{names[i]} - {names[j]}"
            pair_scores[key] = float(sim_matrix[i][j])

    result = {
        "team_success_rate": round(success_rate, 2),
        "positives": list(set(positives)) or ["Нет ярко выраженных плюсов"],
        "negatives": list(set(negatives)) or ["Нет выраженных проблем"],
        "pairwise_scores": pair_scores
    }

    with open("analysis_result.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(text_list, save_path="assets/wordcloud.png"):
    text = " ".join(text_list)
    if not text.strip():
        raise ValueError("Текст пуст — нечего визуализировать.")
    
    wordcloud = WordCloud(width=800, height=400, background_color="white", collocations=False).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    
import seaborn as sns

def generate_heatmap(df, save_path="assets/heatmap.png"):
    if df.empty or "Текст_отзыва" not in df.columns:
        raise ValueError("Невозможно построить heatmap: нет текстов отзывов.")

    cleaned = df["Текст_отзыва"].apply(preprocess)
    X = vectorizer.transform(cleaned)
    sim_matrix = cosine_similarity(X)

    names = df["Имя"].tolist()
    plt.figure(figsize=(8, 6))
    sns.heatmap(sim_matrix, xticklabels=names, yticklabels=names, cmap="Blues", annot=True, fmt=".2f")
    plt.title("Парная совместимость (косинусная близость)")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

