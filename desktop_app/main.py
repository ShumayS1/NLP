# desktop_app/main.py
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
)
import time
import sys
import json
import os
import pandas as pd
import joblib
import docx
import fitz  # PyMuPDF

from logic import run_local_analysis, generate_wordcloud, generate_heatmap
from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Указываем свой шрифт
pdfmetrics.registerFont(TTFont('DejaVu', 'c:\\USERS\\SHUMA\\APPDATA\\LOCAL\\MICROSOFT\\WINDOWS\\FONTS\\DEJAVUSANS.TTF'))




# При создании стиля добавляем наш шрифт
from reportlab.lib.styles import getSampleStyleSheet

# Получаем стиль из стандартного набора
styles = getSampleStyleSheet()

# Создаем новый стиль, клонируя существующий и задавая новый шрифт
normal_style = styles['Normal'].clone('Normal', fontName='DejaVu', fontSize=12)


class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ совместимости команды")
        self.setGeometry(200, 200, 1000, 700)

        layout = QVBoxLayout()

        self.upload_data_btn = QPushButton("Загрузить CSV-файл (Имя, Текст_отзыва, Роль, Команда)")
        self.upload_data_btn.clicked.connect(self.load_data)
        layout.addWidget(self.upload_data_btn)

        self.upload_text_btn = QPushButton("Загрузить TXT, DOCX или PDF для анализа")
        self.upload_text_btn.clicked.connect(self.load_text_file)
        layout.addWidget(self.upload_text_btn)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        buttons = QHBoxLayout()
        self.analyze_btn = QPushButton("Анализировать")
        self.analyze_btn.clicked.connect(self.analyze_team)
        buttons.addWidget(self.analyze_btn)

        self.wordcloud_btn = QPushButton("Показать WordCloud")
        self.wordcloud_btn.clicked.connect(self.show_wordcloud)
        buttons.addWidget(self.wordcloud_btn)

        layout.addLayout(buttons)

        self.result_label = QLabel("Результаты анализа появятся ниже")
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.heatmap_btn = QPushButton("Показать Heatmap")
        self.heatmap_btn.clicked.connect(self.show_heatmap)
        buttons.addWidget(self.heatmap_btn)


        self.setLayout(layout)
        self.data_df = None

        self.export_pdf_btn = QPushButton("Экспорт в PDF")
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)
        buttons.addWidget(self.export_pdf_btn)



    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV-файл с профилями и отзывами", "", "CSV Files (*.csv)")
        if file_path:
            self.data_df = pd.read_csv(file_path)
            self.data_df.to_csv("employee_feedback.csv", index=False)
            self.populate_table(self.data_df)
            QMessageBox.information(self, "Файл загружен", f"Загружено {len(self.data_df)} записей")

    def load_text_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите TXT, DOCX или PDF", "", "Документы (*.txt *.docx *.pdf)")
        text = ""
        if not file_path:
            return

        if file_path.endswith(".txt"):
            with open(file_path, encoding='utf-8') as f:
                text = f.read()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        else:
            QMessageBox.warning(self, "Формат не поддерживается", "Загрузите .txt, .docx или .pdf")
            return

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        entries = []
        for line in lines:
            entries.append({"Имя": "Имя", "Текст_отзыва": line, "Роль": "Роль", "Команда": "Команда"})

        df = pd.DataFrame(entries)
        df.to_csv("employee_feedback.csv", index=False)
        self.data_df = df
        self.populate_table(df)
        QMessageBox.information(self, "Файл подготовлен", f"Извлечено {len(df)} строк для анализа")

    def populate_table(self, df):
        self.table.clear()
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

    def analyze_team(self):
        if self.data_df is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите CSV или документ")
            return

        # Сохраняем возможные изменения из таблицы обратно в CSV
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.data_df.iat[row, col] = self.table.item(row, col).text()

        self.data_df.to_csv("employee_feedback.csv", index=False)

        try:
            run_local_analysis("employee_feedback.csv")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка анализа", str(e))
            return

        if not os.path.exists("analysis_result.json"):
            QMessageBox.warning(self, "Файл не найден", "Файл analysis_result.json не был создан")
            return

        with open("analysis_result.json", encoding='utf-8') as f:
            data = json.load(f)

        success = data.get("team_success_rate", "N/A")
        positives = data.get("positives", [])
        negatives = data.get("negatives", [])
        pairs = data.get("pairwise_scores", {})

        result_str = f"<b>Шанс успешного выполнения проекта:</b> {success * 100:.0f}%<br><br>"
        result_str += "<b>Плюсы команды:</b><br>- " + "<br>- ".join(positives) + "<br><br>"
        result_str += "<b>Минусы команды:</b><br>- " + "<br>- ".join(negatives) + "<br><br>"

        if pairs:
            result_str += "<b>Парная совместимость:</b><br>"
            for pair, score in pairs.items():
                result_str += f"{pair}: {round(score * 100)}%<br>"

        self.result_text.setHtml(result_str)
        try:
            text_list = self.data_df["Текст_отзыва"].dropna().astype(str).tolist()
            generate_wordcloud(text_list)
            generate_heatmap(self.data_df) 
        except Exception as e:
             QMessageBox.warning(self, "WordCloud", f"Не удалось сгенерировать WordCloud: {str(e)}")

    abs_path = os.path.abspath("assets\wordcloud.png")
    os.startfile(abs_path)
    abs_path = os.path.abspath("assets\heatmap.png")
    os.startfile(abs_path)
    def show_wordcloud(self):
        try:
            wordcloud_path = "assets\wordcloud.png"
            time.sleep(1)  # Даем немного времени для записи файла
            if os.path.exists(wordcloud_path):
                os.startfile(wordcloud_path)
            else:
                QMessageBox.warning(self, "Ошибка", "WordCloud ещё не был сгенерирован.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось показать WordCloud: {e}")

    def show_heatmap(self):
        try:
            heatmap_path = "assets\heatmap.png"
            time.sleep(1)  # Даем немного времени для записи файла
            if os.path.exists(heatmap_path):
                os.startfile(heatmap_path)
            else:
                QMessageBox.warning(self, "Ошибка", "Heatmap ещё не был сгенерирован.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось показать Heatmap: {e}")

    def export_to_pdf(self):
        try:
            # Путь для сохранения PDF
            pdf_filename = "analysis_report.pdf"
            
            # Создание PDF документа
            document = SimpleDocTemplate("analysis_report.pdf", pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            styles['Normal'] = styles['Normal'].clone('Normal', fontName='DejaVu', fontSize=12)

            title = Paragraph("Отчёт об анализе совместимости команды", styles['Title'])
            elements.append(title)

            # Результаты анализа
            with open("analysis_result.json", encoding='utf-8') as f:
                data = json.load(f)

                # Добавляем пустую строку после заголовка
                elements.append(Spacer(1, 12))
                
                success = f"Шанс успешного выполнения проекта: {data.get('team_success_rate', 'N/A') * 100:.0f}%"
                success_paragraph = Paragraph(success, styles['Normal'])
                elements.append(success_paragraph)

                # Добавляем пустую строку
                elements.append(Spacer(1, 12))
                
                # Формируем список плюсов с правильным форматированием
                positives_list = data.get('positives', [])
                positives_content = ["<b>Плюсы команды:</b>"] + [f"• {item}" for item in positives_list]
                positives_paragraph = Paragraph("<br/>".join(positives_content), styles['Normal'])
                elements.append(positives_paragraph)

                # Добавляем пустую строку
                elements.append(Spacer(1, 12))
                
                # Формируем список минусов с правильным форматированием
                negatives_list = data.get('negatives', [])
                negatives_content = ["<b>Минусы команды:</b>"] + [f"• {item}" for item in negatives_list]
                negatives_paragraph = Paragraph("<br/>".join(negatives_content), styles['Normal'])
                elements.append(negatives_paragraph)

                # Добавляем пустую строку
                elements.append(Spacer(1, 12))
                
                # Формируем парную совместимость с правильным форматированием
                pair_scores = data.get("pairwise_scores", {})
                pairwise_content = ["<b>Парная совместимость:</b>"] + [f"{pair}: {round(score * 100)}%" for pair, score in pair_scores.items()]
                pairwise_paragraph = Paragraph("<br/>".join(pairwise_content), styles['Normal'])
                elements.append(pairwise_paragraph)

                # Добавляем пустую строку перед изображениями
                elements.append(Spacer(1, 24))
                
                # Добавление изображений (WordCloud и Heatmap)
                wordcloud_img = os.path.join("assets", "wordcloud.png")  # Более надежный путь
                heatmap_img = os.path.join("assets", "heatmap.png")     # Более надежный путь
                
                # Проверяем существование файлов перед добавлением
                if os.path.exists(wordcloud_img):
                    elements.append(Image(wordcloud_img, 300, 200))
                    elements.append(Spacer(1, 12))  # Добавляем промежуток между изображениями
                
                if os.path.exists(heatmap_img):
                    elements.append(Image(heatmap_img, 300, 200))

                # Генерация PDF
                document.build(elements)

                # Уведомление
                QMessageBox.information(self, "Экспорт в PDF", f"Отчёт успешно экспортирован в {pdf_filename}")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось экспортировать в PDF: {str(e)}")


    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec())