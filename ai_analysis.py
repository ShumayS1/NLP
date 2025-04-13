import joblib
import numpy as np

# Загрузка модели и бинализатора
model = joblib.load("final_working_employee_model.pkl")
mlb = joblib.load("final_working_employee_labels.pkl")

def analyze_with_ai(text):
    """
    Принимает текст сотрудника и возвращает список плюсов и минусов.
    """
    prediction = model.predict([text])
    prediction = np.array(prediction)  # гарантируем, что prediction — numpy-массив
    traits = mlb.inverse_transform(prediction)[0]

    plus_words = ["Ответственность", "Командная работа", "Организованность", "Коммуникабельность"]
    minus_words = ["Прокрастинация", "Избегает конфликтов"]

    pluses = [t for t in traits if t in plus_words]
    minuses = [t for t in traits if t in minus_words]

    return pluses, minuses
