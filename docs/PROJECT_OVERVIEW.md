# Project Overview

This project demonstrates automated processing of Swiss payslips using OCR and
local LLM parsing. It is designed for internal evaluation and for client
presentations.



## Purpose

- Extract text from multilingual payslips
- Convert unstructured OCR text into structured fields
- Demonstrate feasibility using a fully local pipeline
- Provide a simple UI for non-technical users


## OCR Component

1. **PyMuPDF**
   - Extracts text from digital PDFs
2. **Poppler + PDF-to-Image**
   - Converts scanned PDFs into images
3. **Tesseract**
   - Performs multilingual OCR (EN/DE/FR/IT)

This combination ensures high accuracy on both digital and scanned documents.


## LLM Parsing Component (Ollama)

- Model: Mistral (default) or Llama 3
- Purpose: Convert OCR text into structured JSON
- Prompt-controlled behavior using a YAML configuration file
- Fully offline & local



## Streamlit Interface

- Simple front-end for demonstrations
- Upload payslips
- View OCR results
- View JSON output
- Download final JSON



## Data Flow Summary

User Upload → OCR → LLM Parsing → JSON Output → Download


This project is a clean and modular proof-of-concept ready for client demos.