from django.shortcuts import render
from .models import Settings
from graduation_project.models import GraduationProject, Category, Review
from accounts.models import UserProfile
from django.db.models import Count, Prefetch



def home(request):
    projects_main = GraduationProject.objects.all().order_by('-id')[:10]
    category = Category.objects.all()
    reviews = Review.objects.all().order_by('-id')[:7]

       # أكتر 10 دكاترة حاصلين على مشاريع مع المشاريع الخاصة بكل دكتور
    doctors = UserProfile.objects.filter(is_doctor=True).annotate(
        book_count=Count('user__doctor_projects')
    ).prefetch_related(
        Prefetch('user__doctor_projects', queryset=GraduationProject.objects.all(), to_attr='doctor_projects_list')
    ).order_by('-book_count')[:10]
    return render(request,"index.html", {"projects_main": projects_main,
                            "category": category,
                            "reviews" : reviews ,
                            "doctors" : doctors})
