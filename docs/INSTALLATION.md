# Installation Guide

This project extracts text from Swiss payslips using OCR and parses it into
structured JSON using a local LLM (Ollama).

Follow these steps to install and run the system.



## 1. Install Python 3.11
Download:
https://www.python.org/downloads/release/python-3110/

Enable:
- “Add Python to PATH”



## 2. Create & activate a virtual environment

### Windows (PowerShell)
python -m venv venv
venv\Scripts\activate


---

## 3. Install required Python packages

pip install -r requirements.txt



## 4. Install Tesseract OCR

Download Windows installer:
https://github.com/UB-Mannheim/tesseract/wiki

Default install path required:
C:\Program Files\Tesseract-OCR\tesseract.exe


## 5. Install Poppler (PDF → Image conversion)

Download:
https://github.com/oschwartz10612/poppler-windows/releases/

Extract into:
C:\Program Files\poppler-XX\Library\bin

The path must match the one referenced in `ocr_extract.py`.



## 6. Install Ollama (Local LLM)

Download:
https://ollama.com/download

Then install a model:
ollama pull mistral

The selected model name must match `MODEL_NAME` in `app/config.py`.


## 7. Verify all components

Test Tesseract:
tesseract --version

Test Ollama:
ollama run mistral

You are now ready to run the application.

