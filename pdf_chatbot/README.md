# DocuMind — PDF Chatbot (Ollama Edition)

Chat with your PDFs using a **free, fully local AI** — no API key, no internet, no cost.

---

## Quick Setup

### Step 1 — Install Ollama
Download and install from: https://ollama.com/download

### Step 2 — Download an AI model (one-time)
```bash
ollama pull llama3
```
> **Lighter alternatives:** `ollama pull mistral` (~4 GB) or `ollama pull phi3` (~2 GB)

### Step 3 — Start Ollama (keep this terminal open)
```bash
ollama serve
```

### Step 4 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Set up the database
```bash
python manage.py migrate
```

### Step 6 — Create an admin user (optional)
```bash
python manage.py createsuperuser
```

### Step 7 — Run the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser, register an account and start chatting!

---

## Changing the AI Model

Edit `pdf_chatbot/settings.py`:
```python
OLLAMA_MODEL = 'mistral'   # or phi3, gemma, llama3, etc.
```

Or use an environment variable:
```bash
OLLAMA_MODEL=mistral python manage.py runserver
```

---

## Troubleshooting

**"Ollama is not running"** — Make sure you ran `ollama serve` in a terminal and it's still open.

**"model not found"** — Run `ollama pull llama3` (or whichever model you set in settings).

**Slow responses** — Ollama runs on CPU by default. GPU acceleration is automatic if you have a compatible GPU.

---

## Requirements
- Python 3.10+
- Django 4.2+
- PyPDF2
- Pillow
- Ollama running locally
