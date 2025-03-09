from django.shortcuts import render
from django.db.models import Count, Prefetch, Q
from .models import Settings
from graduation_project.models import GraduationProject, Category, Review
from accounts.models import UserProfile
from django.views.decorators.cache import cache_page
from django.db.models import Count



# ___________________________________________________________________________________



def get_top_liked_projects():
    # Fetch the top 10 projects with the most likes
    top_liked_projects = (
        GraduationProject.objects
        .annotate(like_count=Count('likes'))  # Count the number of likes for each project
        .filter(status='accepted')  # Optionally filter only accepted projects
        .prefetch_related('likes')  # Optimize by prefetching related likes
        .order_by('-like_count')[:10]  # Order by like count in descending order and limit to 10
    )
    return top_liked_projects



# ___________________________________________________________________________________


# Cache the page for 1 minute to reduce database load
# @cache_page(60 * 1)  
def home(request):
    # Fetch only accepted projects for the main projects section
    projects_main = (
        GraduationProject.objects
        .filter(status='accepted')
        .select_related('category')  # Optimize by fetching related category data in one query
        .order_by('-id')[:10]
    )

   
    # Fetch the top 10 doctors with the most accepted projects
    doctors = (
        UserProfile.objects
        .filter(is_doctor=True)
        .annotate(
            book_count=Count('user__doctor_projects', filter=Q(user__doctor_projects__status='accepted'))
        )
        .prefetch_related(
            Prefetch(
                'user__doctor_projects',
                queryset=GraduationProject.objects.filter(status='accepted').select_related('category'),
                to_attr='doctor_projects_list'
            )
        )
        .order_by('-book_count')[:10]
    )

    # Fetch the top 10 projects with the most likes
    top_liked_projects = get_top_liked_projects()

  

    return render(request, "index.html", {
        "projects_main": projects_main,
        "top_liked_projects": top_liked_projects,  
        "doctors": doctors,
    })



# ___________________________________________________________________________________

