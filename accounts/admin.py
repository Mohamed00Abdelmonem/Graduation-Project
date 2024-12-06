from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'is_leader')  # أضف is_leader هنا
    search_fields = ('user', 'phone_number' )