import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import PDFDocument, ChatSession, ChatMessage
from .utils import extract_text_from_pdf, ask_ollama


@login_required
def home(request):
    sessions = ChatSession.objects.filter(user=request.user).select_related('document')[:20]
    documents = PDFDocument.objects.filter(user=request.user)
    return render(request, 'chatbot/home.html', {
        'sessions': sessions,
        'documents': documents,
    })


@login_required
def session_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages_qs = session.messages.all()
    sessions = ChatSession.objects.filter(user=request.user).select_related('document')[:20]
    documents = PDFDocument.objects.filter(user=request.user)
    return render(request, 'chatbot/chat.html', {
        'session': session,
        'messages': messages_qs,
        'sessions': sessions,
        'documents': documents,
    })


@login_required
def new_session(request):
    session = ChatSession.objects.create(user=request.user, title='New Chat')
    return redirect('chatbot:session', session_id=session.id)


@login_required
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    return redirect('chatbot:home')


@login_required
@require_POST
def upload_pdf(request):
    """Handle PDF file upload and text extraction."""
    if 'pdf_file' not in request.FILES:
        return JsonResponse({'error': 'No file provided.'}, status=400)

    pdf_file = request.FILES['pdf_file']
    session_id = request.POST.get('session_id')

    if not pdf_file.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)

    max_size = settings.MAX_PDF_SIZE_MB * 1024 * 1024
    if pdf_file.size > max_size:
        return JsonResponse({'error': f'File too large. Max size is {settings.MAX_PDF_SIZE_MB}MB.'}, status=400)

    title = os.path.splitext(pdf_file.name)[0]
    doc = PDFDocument(
        user=request.user,
        title=title,
        file=pdf_file,
        file_size=pdf_file.size,
    )
    doc.save()

    try:
        text, page_count = extract_text_from_pdf(doc.file.path)
        doc.extracted_text = text
        doc.page_count = page_count
        doc.save()
    except Exception as e:
        doc.delete()
        return JsonResponse({'error': f'Failed to read PDF: {str(e)}'}, status=500)

    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            session.document = doc
            session.title = title[:80]
            session.save()
        except ChatSession.DoesNotExist:
            pass

    return JsonResponse({
        'success': True,
        'document': {
            'id': doc.id,
            'title': doc.title,
            'page_count': doc.page_count,
            'file_size': doc.file_size_display(),
        }
    })


@login_required
@require_POST
def send_message(request):
    """Handle chat message and return AI response."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    session_id = data.get('session_id')
    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    session = get_object_or_404(ChatSession, id=session_id, user=request.user)

    # Save user message
    ChatMessage.objects.create(session=session, role='user', content=user_message)

    # Get conversation history (last 10 messages for context, excluding the one we just added)
    history = list(session.messages.order_by('-created_at')[1:11])
    history.reverse()

    # Get PDF context
    pdf_text = ''
    if session.document:
        pdf_text = session.document.extracted_text

    # Get AI response from Ollama
    try:
        ai_response = ask_ollama(
            question=user_message,
            pdf_text=pdf_text,
            conversation_history=history,
            ollama_url=settings.OLLAMA_URL,
            ollama_model=settings.OLLAMA_MODEL,
        )
    except Exception as e:
        ai_response = f"⚠️ Sorry, I encountered an error: {str(e)}"

    # Save AI response
    ai_msg = ChatMessage.objects.create(session=session, role='assistant', content=ai_response)

    # Update session title from first user message
    if session.title == 'New Chat':
        session.title = user_message[:60]
        session.save()

    return JsonResponse({
        'success': True,
        'response': ai_response,
        'message_id': ai_msg.id,
    })


@login_required
@require_POST
def attach_document(request):
    """Attach an existing document to a session."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    session_id = data.get('session_id')
    doc_id = data.get('document_id')

    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    doc = get_object_or_404(PDFDocument, id=doc_id, user=request.user)

    session.document = doc
    session.save()

    return JsonResponse({
        'success': True,
        'document': {
            'id': doc.id,
            'title': doc.title,
            'page_count': doc.page_count,
            'file_size': doc.file_size_display(),
        }
    })
