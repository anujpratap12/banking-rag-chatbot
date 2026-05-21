from pypdf import PdfReader
from docx import Document
import os


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        return ""


def extract_pdf_text(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def extract_docx_text(file_path):

    text = ""

    doc = Document(file_path)

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_txt_text(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()