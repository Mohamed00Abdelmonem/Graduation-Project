from django.contrib import admin
from .models import GraduationProject, Category, Review

# Define a custom ModelAdmin for GraduationProject
class GraduationProjectAdmin(admin.ModelAdmin):
    search_fields = ('title', 'graduation_year', 'category__name')  # Use 'category__name' for ForeignKey fields
    list_display = (
        'title', 
        'graduation_year', 
        'category', 
        'status', 
        'created_at',  # Display the creation date
        'updated_at'   # Display the last update date
    )
    list_filter = ('status', 'graduation_year', 'category')  # Optional: Add filters for easier navigation
    ordering = ('-graduation_year',)  # Optional: Order by graduation year (newest first)
    list_per_page = 50  # Display 50 rows per page

    
# Register the models with their respective admin configurations
admin.site.register(GraduationProject, GraduationProjectAdmin)
admin.site.register(Category)
admin.site.register(Review)