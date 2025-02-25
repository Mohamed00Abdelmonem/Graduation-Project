from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name  = "project"

urlpatterns = [
    path('books/', views.ProjectList, name="ProjectList"),
    path('book/<slug:slug>', views.project_detail, name="project_detail"),
    path('project/<slug:slug>/update/', views.UpdateProject.as_view(), name='update_project'),  # تأكد من اسم الرابط
    path('book/<slug:slug>/add-review/', views.add_review, name='add_review'),
    path('projects/<slug:slug>/delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('add-project', views.AddProject.as_view(), name="add_project"),
    path('project/success/', TemplateView.as_view(template_name='success_create_project.html'), name='success_create_project'),    
    path('like/<int:id>', views.like_post, name='like_post'),
    path('approve-project/<int:project_id>/', views.approve_project, name='approve_project'),
    path('reject-project/<int:project_id>/', views.reject_project, name='reject_project'),
    path('pending_projects/', views.pending_projects, name='pending_projects'),


]