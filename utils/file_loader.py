
from PyPDF2 import PdfReader
from docx import Document

def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
