from django.shortcuts import render
from django.db.models import Count, Prefetch, Q  # Import Q here
from .models import Settings
from graduation_project.models import GraduationProject, Category, Review
from accounts.models import UserProfile

def home(request):
    # Fetch only accepted projects for the main projects section
    projects_main = GraduationProject.objects.filter(status='accepted').order_by('-id')[:10]

    # Fetch all categories
    category = Category.objects.all()

    # Fetch the latest 7 reviews
    reviews = Review.objects.all().order_by('-id')[:7]

    # Fetch the top 10 doctors with the most projects (only accepted projects)
    doctors = UserProfile.objects.filter(is_doctor=True).annotate(
        book_count=Count('user__doctor_projects', filter=Q(user__doctor_projects__status='accepted'))  # Use Q here
    ).prefetch_related(
        Prefetch(
            'user__doctor_projects',
            queryset=GraduationProject.objects.filter(status='accepted'),  # Only fetch accepted projects
            to_attr='doctor_projects_list'
        )
    ).order_by('-book_count')[:10]

    return render(request, "index.html", {
        "projects_main": projects_main,
        "category": category,
        "reviews": reviews,
        "doctors": doctors,
    })