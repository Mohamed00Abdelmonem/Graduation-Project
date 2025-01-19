from django.shortcuts import render
from graduation_project.models import GraduationProject

def home(request):
    user = request.user
    pending_projects = GraduationProject.objects.filter(status='pending')
    pending_projects_count = pending_projects.count()

    context = {
        'user': user,
        'pending_projects_count': pending_projects_count,
    }
    return (context)