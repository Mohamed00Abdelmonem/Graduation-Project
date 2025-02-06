from django.shortcuts import render
from graduation_project.models import GraduationProject
from django.db.models import Count

def home(request):
    user = request.user

    # Use annotate and aggregate to calculate the count in a single query
    pending_projects_count = (
        GraduationProject.objects
        .filter(status='pending')
        .aggregate(count=Count('id'))  # Use 'id' as it's always unique
        .get('count', 0)  # Default to 0 if no pending projects exist
    )

    context = {
        'user': user,
        'pending_projects_count': pending_projects_count,
    }

    return context