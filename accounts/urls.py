from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/', views.Profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/experience/add/', views.add_experience, name='add_experience'),
    path('profile/experience/update/<int:experience_id>/', views.update_experience, name='update_experience'),
    path('profile/experience/delete/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    
    path('upload/', views.upload_excel, name='upload_excel'),  # Upload Excel file
    path('login/', views.national_id_login, name='login'),     # Login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Logout
    path('', views.home, name='home'),  # Home page
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)