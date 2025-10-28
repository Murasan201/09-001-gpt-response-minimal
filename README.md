# 09-001-gpt-response-minimal

Minimal quickstart to call OpenAI's ChatGPT once and print the reply (Python + .env). This is a preparatory step for a Raspberry Pi news board project.

## Setup
```bash
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-...
```
(Optional) Secure the file on Unix-like systems:
```bash
chmod 600 .env
```

## Run
```bash
python3 api_test.py
```
