import re
import urllib.request
import json


def extract_text_from_pdf(pdf_path: str) -> tuple:
    """Extract text from a PDF file. Returns (text, page_count)."""
    try:
        import PyPDF2
        text_parts = []
        page_count = 0
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            page_count = len(reader.pages)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n\n'.join(text_parts), page_count
    except ImportError:
        pass

    # Fallback basic extraction
    with open(pdf_path, 'rb') as f:
        raw = f.read()
    page_count = raw.count(b'/Type /Page') or 1
    text_parts = []
    for part in raw.split(b'stream')[1:]:
        end = part.find(b'endstream')
        if end == -1:
            continue
        readable = re.sub(rb'[^\x20-\x7E\n\r\t]', b' ', part[:end])
        cleaned = ' '.join(readable.decode('ascii', errors='ignore').split())
        if len(cleaned) > 20:
            text_parts.append(cleaned)
    return ' '.join(text_parts)[:50000], page_count


def ask_ollama(
    question: str,
    pdf_text: str,
    conversation_history: list,
    ollama_url: str = 'http://localhost:11434',
    ollama_model: str = 'llama3',
) -> str:
    """Send a question to the local Ollama instance and return the response."""

    if pdf_text:
        system = (
            "You are an intelligent PDF assistant. Use the document content below "
            "to answer the user's questions accurately. If the answer is not in the "
            "document, say so clearly. Format responses using markdown when helpful.\n\n"
            "=== PDF DOCUMENT CONTENT ===\n"
            + pdf_text[:3000]
            + "\n=== END OF DOCUMENT ==="
        )
    else:
        system = (
            "You are a helpful AI assistant. No PDF has been uploaded yet. "
            "Answer general questions and encourage the user to upload a PDF "
            "for document-specific answers."
        )

    # Build message list
    messages = [{"role": "system", "content": system}]
    for msg in conversation_history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": question})

    payload = json.dumps({
        "model": ollama_model,
        "stream": False,
        "messages": messages,
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{ollama_url.rstrip('/')}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['message']['content']
    except ConnectionRefusedError:
        return (
            "⚠️ **Ollama is not running.** Please open a terminal and run:\n\n"
            "```\nollama serve\n```\n\n"
            "Then try again. If you haven't installed Ollama yet, download it from https://ollama.com/download"
        )
    except urllib.error.URLError as e:
        reason = str(e.reason) if hasattr(e, 'reason') else str(e)
        if 'Connection refused' in reason or 'refused' in reason.lower():
            return (
                "⚠️ **Ollama is not running.** Please open a terminal and run:\n\n"
                "```\nollama serve\n```\n\nThen try again."
            )
        return f"⚠️ Connection error: {reason}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"
