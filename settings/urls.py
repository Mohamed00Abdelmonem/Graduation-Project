from django.urls import path
from .views import home, about
urlpatterns = [
    path('', home),
    path('about', about),
]