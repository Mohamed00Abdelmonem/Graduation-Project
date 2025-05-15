from django.urls import path
from .views import home, about
# , generate_ollama_text, ollama_page
urlpatterns = [
    path('', home),
    path('about', about),
    # path('ai/', ollama_page, name='ai'),  # صفحة الـ HTML
    # path('generate/', generate_ollama_text, name='generate'),  # API Post فقط
]