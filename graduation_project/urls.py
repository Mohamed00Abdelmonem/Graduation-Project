from django.urls import path
from . import views

app_name  = "project"

urlpatterns = [
    path('book/<int:pk>', views.ProjectDetail.as_view(), name="project_detail"),
    path('add-project', views.AddProject.as_view(), name="add_project"),
    path('like/<int:id>', views.like_post, name='like_post'),


]