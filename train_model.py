
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Пример обучающих данных (можно заменить загрузкой из файла в будущем)
X = [
    "Я ответственный и всегда довожу дело до конца",
    "Мне сложно работать в условиях стресса",
    "Организованный, люблю порядок в задачах",
    "Иногда откладываю важное на потом",
    "Коммуникабельный, легко вхожу в команду",
    "Быстро устаю, если работа однообразная",
]
y = [
    ["ответственный"],
    ["минус_стресс"],
    ["организованный"],
    ["минус_прокрастинация"],
    ["коммуникабельный"],
    ["минус_усталость"]
]

mlb = MultiLabelBinarizer()
y_bin = mlb.fit_transform(y)

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultiOutputClassifier(LogisticRegression(max_iter=1000)))
])

model.fit(X, y_bin)

# Сохраняем модель и мультибинаризатор
with open("final_working_employee_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("final_working_employee_labels.pkl", "wb") as f:
    pickle.dump(mlb, f)

print("✅ Модель обучена и сохранена!")
