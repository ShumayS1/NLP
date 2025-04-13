
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QFileDialog, QHBoxLayout
from gui.plot import plot_radar_chart
from utils.file_loader import read_file
from nlp.analyzer import analyze_multiple

class CompatibilityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ совместимости сотрудников")
        self.inputs = []
        self.labels = []

        self.num_select = QComboBox()
        self.num_select.addItems([str(i) for i in range(2, 5)])
        self.num_select.currentIndexChanged.connect(self.update_fields)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Выберите количество сотрудников:"))
        self.layout.addWidget(self.num_select)

        self.fields_layout = QVBoxLayout()
        self.layout.addLayout(self.fields_layout)

        self.analyze_btn = QPushButton("Анализировать")
        self.analyze_btn.clicked.connect(self.analyze)
        self.layout.addWidget(self.analyze_btn)

        self.result_label = QLabel("Результаты появятся здесь...")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.update_fields()

    def update_fields(self):
        # Очистка предыдущих полей
        for i in reversed(range(self.fields_layout.count())):
            self.fields_layout.itemAt(i).widget().setParent(None)
        self.inputs = []
        self.labels = []

        num = int(self.num_select.currentText())
        for i in range(num):
            label = QLabel(f"Сотрудник {i+1}:")
            text_input = QTextEdit()
            load_btn = QPushButton(f"Загрузить файл {i+1}")
            load_btn.clicked.connect(lambda _, idx=i, input_box=text_input: self.load_file(idx, input_box))

            self.fields_layout.addWidget(label)
            self.fields_layout.addWidget(text_input)
            self.fields_layout.addWidget(load_btn)

            self.inputs.append(text_input)
            self.labels.append(label)

    def load_file(self, index, input_box):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Документы (*.txt *.pdf *.docx)")
        if path:
            content = read_file(path)
            input_box.setText(content)

    def analyze(self):
        texts = [inp.toPlainText() for inp in self.inputs]
        result_text, compatibility_scores = analyze_multiple(texts)
        self.result_label.setText(result_text)
        plot_radar_chart(compatibility_scores, [f"Сотрудник {i+1}" for i in range(len(texts))])
