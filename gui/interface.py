
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout, QTabWidget, QMessageBox
from utils.file_loader import read_file
from nlp.analyzer import analyze_multiple
from export_log import save_analysis_result
import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class CompatibilityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ совместимости сотрудников")
        self.resize(900, 700)

        self.text_edits = []
        self.file_buttons = []

        layout = QVBoxLayout()

        for i in range(4):
            row = QHBoxLayout()
            text_edit = QTextEdit()
            text_edit.setPlaceholderText(f"Введите текст сотрудника {i + 1}...")
            self.text_edits.append(text_edit)

            file_btn = QPushButton(f"Загрузить файл {i + 1}")
            file_btn.clicked.connect(lambda _, x=i: self.load_file(x))
            self.file_buttons.append(file_btn)

            row.addWidget(QLabel(f"Сотрудник {i + 1}:"))
            row.addWidget(text_edit)
            row.addWidget(file_btn)
            layout.addLayout(row)

        self.analyze_btn = QPushButton("Анализировать")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)

        self.retrain_btn = QPushButton("Переобучить модель на текущих данных")
        self.retrain_btn.clicked.connect(self.retrain_model)
        layout.addWidget(self.retrain_btn)

        self.tabs = QTabWidget()
        self.results_tab = QTextEdit()
        self.results_tab.setReadOnly(True)
        self.compatibility_tab = QTextEdit()
        self.compatibility_tab.setReadOnly(True)
        self.history_tab = QTextEdit()
        self.history_tab.setReadOnly(True)

        self.tabs.addTab(self.results_tab, "Результаты")
        self.tabs.addTab(self.compatibility_tab, "Совместимость")
        self.tabs.addTab(self.history_tab, "История анализа")

        self.show_history()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def load_file(self, index):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt *.docx *.pdf)")
        if path:
            content = read_file(path)
            self.text_edits[index].setText(content)

    def analyze(self):
        texts = [edit.toPlainText() for edit in self.text_edits if edit.toPlainText().strip()]
        if len(texts) < 2:
            self.results_tab.setText("⚠️ Введите как минимум 2 текста для анализа.")
            return

        result_data, compatibility_scores = analyze_multiple(texts)

        results = ""
        for i, person in enumerate(result_data):
            results += f"Сотрудник {i + 1}:"
            results += f"🔹 Плюсы: {', '.join(person['pluses']) if person['pluses'] else '—'}"
            results += f"🔻 Минусы: {', '.join(person['minuses']) if person['minuses'] else '—'}"
            results += f"📊 Тональность: {person['sentiment']:.2f}"

        compatibility = ""
        for pair, score in compatibility_scores:
            compatibility += f"Сотрудник {pair[0] + 1} и Сотрудник {pair[1] + 1}: {score:.1f}%"

        self.results_tab.setText(results)
        self.compatibility_tab.setText(compatibility)

        entries = []
        for i, text in enumerate(texts):
            entry = {
                "text": text,
                "pluses": result_data[i]["pluses"],
                "minuses": result_data[i]["minuses"],
                "sentiment": result_data[i]["sentiment"],
                "labels": result_data[i]["pluses"] + [f"минус_{m}" for m in result_data[i]["minuses"]]
            }
            entries.append(entry)

        save_analysis_result(texts, result_data, compatibility_scores)
        pd.DataFrame(entries).to_csv("analysis_history.csv", index=False)
        self.show_history()

    def retrain_model(self):
        texts = [edit.toPlainText().strip() for edit in self.text_edits if edit.toPlainText().strip()]
        if not texts:
            QMessageBox.warning(self, "Нет данных", "Заполните хотя бы одно поле для переобучения.")
            return

        with open("retrain_input.txt", "w", encoding="utf-8") as f:
            for text in texts:
                f.write(text.strip() + "\n")

        try:
            subprocess.run([sys.executable, "train_model.py"], check=True)
            QMessageBox.information(self, "Готово", "✅ Модель переобучена на текущих текстах!")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Ошибка", "❌ Не удалось переобучить модель.")

    def show_history(self):
        try:
            df = pd.read_csv("analysis_history.csv")
            self.history_tab.setText(df.to_string(index=False))
        except Exception as e:
            self.history_tab.setText("❌ Ошибка при загрузке истории: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompatibilityApp()
    window.show()
    sys.exit(app.exec_())
