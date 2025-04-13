import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline

MODEL_FILE = "final_working_employee_model.pkl"
LABELS_FILE = "final_working_employee_labels.pkl"
TRAIN_DATA_FILE = "train_data.csv"


def load_data():
    df = pd.read_csv(TRAIN_DATA_FILE)
    df["labels"] = df["labels"].apply(eval)  # Преобразуем строку обратно в список
    return df


def train_model():
    df = load_data()
    X = df["text"]
    y = df["labels"]

    mlb = MultiLabelBinarizer()
    y_bin = mlb.fit_transform(y)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=1000)),
        ("clf", MultiOutputClassifier(LogisticRegression(max_iter=1000)))
    ])

    pipeline.fit(X, y_bin)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(pipeline, f)

    with open(LABELS_FILE, "wb") as f:
        pickle.dump(mlb, f)

    print("✅ Модель и бинализатор сохранены!")


if __name__ == "__main__":
    train_model()
