# Run Guide

This document describes how to run the payslip extraction demo.



## 1. Activate the virtual environment
venv\Scripts\activate



## 2. Confirm Ollama is running

You can test with:
ollama run mistral


If you see an interactive prompt, it works.



## 3. Start the Streamlit application

From the project root:
streamlit run app/app.py


Your browser will open automatically:

http://localhost:8501



## 4. How to use the interface

1. Upload a payslip (PDF / JPG / PNG)
2. OCR extracts raw text
3. Local LLM converts extracted text to structured JSON
4. JSON appears in the interface
5. You may download the JSON file



## 5. Output storage

By default, no files are auto-saved.  

If desired, processed files can be stored manually in:

data/payslips_output/


This is the complete end-to-end flow for running the demonstration.