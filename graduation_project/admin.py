from django.contrib import admin
from .models import GraduationProject, User, Category, Review
# Register your models here.


admin.site.register(GraduationProject)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Review)