from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', lambda request: redirect('chatbot:home' if request.user.is_authenticated else 'accounts:login')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
