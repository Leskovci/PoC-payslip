import json
import requests
import os
from datetime import datetime
import re
import yaml

# Load from config.py (DO NOT override later!)
from config import OLLAMA_URL, MODEL_NAME


# Load extraction prompt from YAML
def load_prompt():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "prompts", "prompt_config.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config["payslip_prompt"]


# Normalize Swiss salary formats
def normalize_salary(value):
    if not value or not isinstance(value, str):
        return ""

    value = value.strip()

    swiss_pattern = r"^\d{1,3}([\'’ ]\d{3})*(\.\d{2})?$"
    decimal_pattern = r"^\d+[\.,]\d{2}$"

    if re.match(swiss_pattern, value) or re.match(decimal_pattern, value):
        cleaned = value.replace("’", "'").replace(" ", "")
        return cleaned

    if re.fullmatch(r"\d+", value):
        return value

    return value


# Query Ollama
def query_ollama(prompt):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "top_k": 1,
                "top_p": 0.1,
                "repeat_penalty": 1.0
            }
        }

        print(f"[LLM] Sending request to: {OLLAMA_URL}")

        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        print(f"[LLM ERROR] Ollama query failed: {e}")
        return ""


# Main extraction pipeline
def parse_payslip_with_llm(text, filename):
    base_prompt = load_prompt()

    final_prompt = f"""
{base_prompt}

PDF Name: {filename}

Text to analyze:
{text}
"""

    print(f"[LLM] Calling model: {MODEL_NAME}")
    result = query_ollama(final_prompt)

    if not result:
        print("[LLM] Empty response returned")
        return {"raw_response": "", "PDF Name": filename}

    # Parse JSON output
    try:
        parsed = json.loads(result)
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
    except Exception as e:
        print(f"[LLM ERROR] Could not parse returned JSON: {e}")
        return {"raw_response": result}

    structured = {
        "Employer Name": parsed.get("Employer Name", ""),
        "Employer Address": parsed.get("Employer Address", ""),
        "Employee Name": parsed.get("Employee Name", ""),
        "Employee Address": parsed.get("Employee Address", ""),
        "Payslip Period": parsed.get("Payslip Period", ""),
        "Salary Gross Amount": normalize_salary(parsed.get("Salary Gross Amount", "")),
        "Salary Net Amount": normalize_salary(parsed.get("Salary Net Amount", "")),
        "Social Security Number": parsed.get("Social Security Number", ""),
        "PDF Name": filename,
        "PDF Path": "UploadedFile",
        "Date of Execution": datetime.now().isoformat(timespec="minutes")
    }

    return structured
