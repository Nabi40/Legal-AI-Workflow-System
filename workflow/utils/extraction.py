import os
import re
from PIL import Image
from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path


def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(file_path):
    text = ""

    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    except Exception:
        return ""

    return text


def ocr_pdf(file_path):
    text = ""

    try:
        pages = convert_from_path(file_path, dpi=250)
        for i, page in enumerate(pages):
            page_text = pytesseract.image_to_string(page)
            text += f"\n--- Page {i + 1} OCR ---\n{page_text}"
    except Exception as e:
        text += f"\n[OCR_FAILED: {str(e)}]"

    return text


def ocr_image(file_path):
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[IMAGE_OCR_FAILED: {str(e)}]"


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_pdf_text(file_path)

        if len(text.strip()) < 100:
            text = ocr_pdf(file_path)

        return clean_text(text)

    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return clean_text(ocr_image(file_path))

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return clean_text(f.read())

    return ""