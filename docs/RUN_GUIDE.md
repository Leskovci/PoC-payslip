Run Guide

This document describes how to run the payslip extraction demo using Docker.

1. Start the complete system (LLM + App)

From the project root (where docker-compose.yml is located), run:

docker compose build
docker compose up -d


This command:

Starts Ollama (local LLM server)

Starts the Streamlit application

Sets up OCR, Azure Blob access, and internal networking

Both services run together automatically.

2. Confirm Ollama is running

You can test by opening a shell inside the Ollama container:

docker exec -it ollama_server bash


Then run:

ollama run mistral:7b-instruct-q4_K_M "Hello"


If the model responds, the LLM is working.

Type exit to leave the shell.

3. Open the Streamlit application

After the containers are running, open:

http://localhost:8501


This loads the user interface in your browser.

4. How to use the interface

Upload a payslip (PDF / JPG / PNG), or select one from Azure Blob

OCR extracts text inside the container

The local LLM (via Ollama) converts the extracted text into structured JSON

The JSON result is displayed in the interface

You can download the JSON or CSV

Results are also saved to Azure Blob Storage

5. Azure Blob Storage integration

Uploaded files are stored in:

inputfiles/


Extracted JSON outputs are stored in:

outputfiles/


You can manage these files using:

Azure Portal

Azure CLI

The provided blob_test.py tool

6. Stopping the system

To stop all containers:

docker compose down

7. Updating the system after code changes

After modifying the source code:

docker compose down
docker compose build --no-cache
docker compose up -d


This rebuilds the Streamlit application container with your latest changes.