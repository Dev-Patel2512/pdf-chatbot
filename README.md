# 🧠 DocuMind — AI PDF Chatbot

A Django-based web application that lets you **chat with your PDF documents** using a completely **free, local AI** powered by Ollama. No API key required, no internet needed for AI, no cost!

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 📄 Upload PDF documents and chat with them
- 🤖 Powered by local AI via Ollama (completely free)
- 💬 Full conversation history saved automatically
- 👤 User authentication (register/login)
- 📚 Multiple PDFs and chat sessions
- 🌙 Beautiful dark UI
- 🔒 No API key needed — runs 100% on your PC

---

## 🖥️ Screenshots

> Upload a PDF → Ask questions → Get AI answers instantly

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2
- **AI:** Ollama (phi3 / llama3 / mistral)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (no framework)
- **PDF Reading:** PyPDF2

---

## ⚙️ Requirements

- Python 3.10 or higher
- Ollama installed on your PC
- 4GB+ RAM (8GB recommended)
- Windows / Mac / Linux

---

## 🚀 Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/documind.git
cd documind/pdf_chatbot
```

### Step 2 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 3 — Install Ollama
Download and install from: https://ollama.com/download

### Step 4 — Download an AI model (one time only)
```bash
# Recommended (small and fast, 2.2 GB)
ollama pull phi3

# OR better quality (4.7 GB)
ollama pull llama3

# OR medium option (4 GB)
ollama pull mistral
```

### Step 5 — Set your model in settings
Open `pdf_chatbot/settings.py` and set:
```python
OLLAMA_MODEL = 'phi3'   # change to whichever model you downloaded
```

### Step 6 — Setup the database
```bash
python manage.py migrate
```

### Step 7 — Create your account
```bash
python manage.py createsuperuser
```
Enter your username, phone number, and password when prompted.

### Step 8 — Run the app
```bash
python manage.py runserver
```

### Step 9 — Open in browser
```
http://127.0.0.1:8000
```

---

## 📅 How to Run Every Day

```bash
# Terminal 1 — Ollama runs automatically in background (nothing to do!)

# Terminal 2 — Start the Django server
cd path/to/pdf_chatbot
python manage.py runserver
```

Then open: http://127.0.0.1:8000

---

## 💡 Tips for Better Performance

- Close unnecessary apps and browser tabs before chatting
- First AI response takes 2-3 minutes on CPU — be patient
- After the first response, it gets faster
- Use a GPU PC for much faster responses
- Ask short, specific questions for best results

---

## 📁 Project Structure

```
pdf_chatbot/
├── accounts/           # User authentication (register, login, logout)
│   ├── models.py       # CustomUser model
│   ├── views.py        # Register, login, logout views
│   └── forms.py        # Registration and login forms
├── chatbot/            # Main chat application
│   ├── models.py       # PDFDocument, ChatSession, ChatMessage models
│   ├── views.py        # Chat, upload, send message views
│   └── utils.py        # PDF extraction + Ollama AI integration
├── pdf_chatbot/        # Django project settings
│   ├── settings.py     # Configuration (Ollama model, DB, etc.)
│   └── urls.py         # URL routing
├── templates/          # HTML templates
│   ├── base.html       # Base template with dark UI
│   ├── accounts/       # Login and register pages
│   └── chatbot/        # Chat UI, sidebar, home page
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration

All settings are in `pdf_chatbot/settings.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `phi3` | AI model to use |
| `MAX_PDF_SIZE_MB` | `10` | Max PDF upload size |

---

## 🤖 Supported AI Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `phi3` | 2.2 GB | ⚡ Fast | Good |
| `mistral` | 4 GB | Medium | Better |
| `llama3` | 4.7 GB | Slower | Best |

---

## ❓ Troubleshooting

**"Ollama is not running" error**
```bash
ollama serve
```

**"timed out" error**
- Close other apps to free RAM
- Ask a shorter/simpler question
- Wait longer — first response is always slow

**"model not found" error**
```bash
ollama pull phi3
```

**Check which models are downloaded**
```bash
ollama list
```

---

## 📦 Dependencies

```
Django>=4.2,<5.0
PyPDF2>=3.0.0
Pillow>=10.0.0
```

---

## 🙌 Contributing

Pull requests are welcome! Feel free to open an issue for bugs or feature requests.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Made with ❤️ using Django + Ollama
