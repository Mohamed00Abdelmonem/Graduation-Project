from django.urls import path
from .views import log_list_view, logs_chart_view

urlpatterns = [
    path('logs/', log_list_view, name='logs_list'),
    path('logs_chart_view/', logs_chart_view, name='logs_chart_view'),
]
