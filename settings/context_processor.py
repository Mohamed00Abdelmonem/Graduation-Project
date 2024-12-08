# from django.shortcuts import render
# from .models import Settings
# from graduation_project.models import GraduationProject, Category, Review
# from accounts.models import UserProfile

# def home(request):
#     projects_main = GraduationProject.objects.all()[10:]
#     category = Category.objects.all()
#     reviews = Review.objects.latest(6)
#     doctors = UserProfile.objects.filter(is_doctor=True)
#     return render(request, {"projects_main": projects_main,
#                             "category": category,
#                             "reviews" : reviews ,
#                             "doctors" : doctors})
