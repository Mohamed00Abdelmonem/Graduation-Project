from django.urls import path
from . import views

app_name  = "project"

urlpatterns = [
    path('books/', views.ProjectList, name="ProjectList"),
    path('book/<slug:slug>', views.ProjectDetail.as_view(), name="project_detail"),
    path('add-project', views.AddProject.as_view(), name="add_project"),
    path('like/<int:id>', views.like_post, name='like_post'),
    path('approve-project/<int:project_id>/', views.approve_project, name='approve_project'),
    path('reject-project/<int:project_id>/', views.reject_project, name='reject_project'),
    path('pending_projects/', views.pending_projects, name='pending_projects'),


]