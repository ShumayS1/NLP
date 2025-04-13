import pickle
import numpy as np

MODEL_FILE = "final_working_employee_model.pkl"
LABELS_FILE = "final_working_employee_labels.pkl"


with open(MODEL_FILE, "rb") as f:
    model = pickle.load(f)

with open(LABELS_FILE, "rb") as f:
    mlb = pickle.load(f)


def analyze_with_ai(text):
    prediction = model.predict([text])
    predicted_labels = mlb.inverse_transform(prediction)[0] if np.sum(prediction) > 0 else []

    pluses = [label for label in predicted_labels if label.startswith("plus:")]
    minuses = [label for label in predicted_labels if label.startswith("minus:")]
    sentiment = sum(1 for label in predicted_labels if label.startswith("plus:")) - \
                sum(1 for label in predicted_labels if label.startswith("minus:"))

    return pluses, minuses, sentiment