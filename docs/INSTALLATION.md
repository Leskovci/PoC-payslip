Installation Guide

This project extracts text from Swiss payslips using OCR and parses it into
structured JSON using a local LLM (Ollama), all running inside Docker.

Follow these steps to install and run the system.

1. Install Docker & Docker Compose
Windows (Docker Desktop)

Download Docker Desktop:
https://www.docker.com/products/docker-desktop/

Install it and ensure:

“Use WSL 2 based engine” is enabled (recommended)

Docker Desktop is running

To verify:

docker --version
docker compose version


If both commands show a version number, Docker is ready.

2. Get the project code

Clone or copy the project repository to your machine.

Example (Git):

git clone <YOUR_REPO_URL> payslip_extraction_poc
cd payslip_extraction_poc


Make sure this folder contains:

docker-compose.yml

Dockerfile

requirements.txt

app/ directory (Streamlit, OCR, LLM code)

app/prompts/prompt_config.yaml

app/config.py

3. Configure Azure connection (if needed)

The Azure Blob Storage connection string is defined in:

app/config.py (or a similar config file)

Make sure:

AZURE_CONNECTION_STRING = "your-connection-string-here"


is set to a valid value for your Azure Storage account.

For local testing without Azure, you can leave it as-is, but Azure features (input/output blobs) will not work.

4. Build the Docker images

From the project root folder (where docker-compose.yml lives), run:

docker compose build


This will:

Build the Streamlit app image

Prepare the Ollama service container

5. Start the full system (App + LLM)

Still in the project root, run:

docker compose up -d


This will:

Start the Ollama container (LLM server)

Start the Streamlit container (UI + OCR + Azure integration)

Create an internal Docker network

Expose:

Streamlit UI on port 8501

Ollama API on port 11434

To verify:

docker compose ps


You should see both ollama_server and payslip_app in “Up” state.

6. Ensure the LLM model is available

If the model was not pulled automatically, you can enter the Ollama container and pull it manually.

docker exec -it ollama_server bash


Inside the container:

ollama pull mistral:7b-instruct-q4_K_M
ollama run mistral:7b-instruct-q4_K_M "Hello"


If you see a response, the LLM is ready.

Type exit to leave the container shell.

7. Access the application

Open your browser and go to:

http://localhost:8501


(or http://<SERVER_IP>:8501 if running on a remote VM)

You should now see the payslip extraction interface.

8. Optional: Stop and restart the system

To stop all containers:

docker compose down


To rebuild and start again after code changes:

docker compose down
docker compose build --no-cache
docker compose up -d