from django.contrib import admin
from .models import UserProfile, Experience

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address', 'is_leader')  
    search_fields = ('user', 'phone_number' )


admin.site.register(Experience)