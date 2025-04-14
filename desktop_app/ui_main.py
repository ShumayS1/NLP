import pandas as pd

def load_feedback(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    assert {'Имя', 'Текст_отзыва', 'Роль', 'Команда'}.issubset(df.columns), "Некорректный формат файла"
    return df
