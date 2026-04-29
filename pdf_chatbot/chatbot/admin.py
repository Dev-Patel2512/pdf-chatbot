from django.contrib import admin
from .models import PDFDocument, ChatSession, ChatMessage


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'page_count', 'file_size', 'uploaded_at']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['title', 'user__username']


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['role', 'content', 'created_at']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'document', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    inlines = [ChatMessageInline]
