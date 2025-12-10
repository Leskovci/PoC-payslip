import os
from io import BytesIO
from PIL import Image, ImageFilter, ImageOps
import pytesseract
from pdf2image import convert_from_bytes
import fitz  # PyMuPDF
import numpy as np

# Detect environment: Windows vs Linux inside Docker
if os.name == "nt":
    # Windows path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    # Linux path (Docker)
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def preprocess_image(img):
    # Convert to grayscale
    img = ImageOps.grayscale(img)

    # Increase contrast
    img = ImageOps.autocontrast(img)

    # Sharpen to improve OCR identification
    img = img.filter(ImageFilter.SHARPEN)

    # Convert to numpy for advanced transforms
    arr = np.array(img)

    # Binarization (threshold)
    arr = np.where(arr > 160, 255, 0).astype("uint8")

    # Back to image
    img = Image.fromarray(arr)

    return img


def extract_text(file_input):
    """
    Improved OCR:
    - First tries PyMuPDF text extraction (for text PDFs)
    - If empty, fallback to OCR
    - Image preprocessing for more accurate OCR
    """

    text = ""

    try:
        if isinstance(file_input, BytesIO):
            file_input.seek(0)
            data = file_input.read()

            # Try text-based PDF
            try:
                pdf = fitz.open(stream=data, filetype="pdf")
                for page in pdf:
                    page_text = page.get_text("text")
                    if isinstance(page_text, str):
                        text += page_text
                pdf.close()

                if text.strip():
                    return clean_extracted_text(text)

            except Exception:
                pass

            # OCR fallback (PDF scanned pages)
            try:
                pages = convert_from_bytes(data, dpi=250)
                for page in pages:
                    processed = preprocess_image(page)
                    ocr_text = pytesseract.image_to_string(
                        processed,
                        lang="eng+fra+deu+ita",
                        config="--oem 3 --psm 6"
                    )
                    text += ocr_text

            except Exception:
                # Try image directly
                try:
                    img = Image.open(BytesIO(data))
                    processed = preprocess_image(img)
                    text = pytesseract.image_to_string(
                        processed,
                        lang="eng+fra+deu+ita",
                        config="--oem 3 --psm 6"
                    )
                except:
                    return ""

            return clean_extracted_text(text)

        else:
            return ""

    except Exception:
        return ""


def clean_extracted_text(text):
    text = text.replace("|", " ")
    text = text.replace("•", " ")
    text = text.replace("\t", " ")
    text = text.replace("\xad", "")  # hyphenation removal
    text = " ".join(text.split())  # collapse multiple whitespace
    return text.strip()
