
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel

class CompatibilityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ совместимости сотрудников")

        self.input1 = QTextEdit()
        self.input2 = QTextEdit()
        self.button = QPushButton("Анализировать")
        self.result = QLabel("Результат появится здесь...")

        self.button.clicked.connect(self.analyze)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Сотрудник 1:"))
        layout.addWidget(self.input1)
        layout.addWidget(QLabel("Сотрудник 2:"))
        layout.addWidget(self.input2)
        layout.addWidget(self.button)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def analyze(self):
        text1 = self.input1.toPlainText()
        text2 = self.input2.toPlainText()

        from nlp.analyzer import analyze_texts
        result = analyze_texts(text1, text2)

        self.result.setText(result)
