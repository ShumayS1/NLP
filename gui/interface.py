
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel,
    QHBoxLayout, QFileDialog, QApplication, QTabWidget, QGridLayout, QSizePolicy
)
from nlp.analyzer import analyze_multiple
from utils.file_loader import read_file

class CompatibilityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ совместимости сотрудников")
        self.setGeometry(100, 100, 1000, 800)

        self.text_edits = []
        self.file_buttons = []

        main_layout = QVBoxLayout()
        form_layout = QGridLayout()

        for i in range(4):
            label = QLabel(f"Сотрудник {i+1}:")
            text_edit = QTextEdit()
            text_edit.setPlaceholderText(f"Введите текст сотрудника {i+1}...")
            file_button = QPushButton("📁 Загрузить")
            file_button.clicked.connect(lambda checked, idx=i: self.load_file(idx))

            self.text_edits.append(text_edit)
            self.file_buttons.append(file_button)

            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(text_edit, i, 1)
            form_layout.addWidget(file_button, i, 2)

        main_layout.addLayout(form_layout)

        self.analyze_button = QPushButton("🚀 Анализировать")
        self.analyze_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.analyze_button.clicked.connect(self.analyze)
        main_layout.addWidget(self.analyze_button)

        self.results_tabs = QTabWidget()
        main_layout.addWidget(self.results_tabs)

        self.setLayout(main_layout)

    def load_file(self, index):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt *.pdf *.docx)")
        if filename:
            text = read_file(filename)
            self.text_edits[index].setText(text)

    def analyze(self):
        self.results_tabs.clear()
        texts = [te.toPlainText().strip() for te in self.text_edits if te.toPlainText().strip()]
        if len(texts) < 2:
            self.results_tabs.addTab(QLabel("Введите хотя бы двух сотрудников."), "Ошибка")
            return

        result_text, compatibility_scores = analyze_multiple(texts)

        # Разбивка по сотрудникам
        lines = result_text.strip().split("\n\n")
        for i, block in enumerate(lines):
            label = QLabel(block.replace("\n", "<br>"))
            label.setWordWrap(True)
            self.results_tabs.addTab(label, f"Сотрудник {i+1}")

        # Совместимость
        compatibility_text = ""
        for pair, score in compatibility_scores.items():
            compatibility_text += f"🤝 {pair} — <b>{score:.1f}%</b><br>"

        compatibility_label = QLabel(compatibility_text)
        compatibility_label.setWordWrap(True)
        self.results_tabs.addTab(compatibility_label, "Совместимость")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CompatibilityApp()
    window.show()
    sys.exit(app.exec())
