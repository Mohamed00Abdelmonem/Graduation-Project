from django.urls import path
from .views import ProjectDetail

urlpatterns = [
    path('book/<int:pk>', ProjectDetail.as_view()),
]