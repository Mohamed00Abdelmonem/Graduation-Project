# excel_project/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
    path('home/', views.upload_excel, name='home'),
    path('login/', views.national_id_login, name='login'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
] 
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)