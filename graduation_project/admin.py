from django.contrib import admin
from .models import GraduationProject, Category, Review, ProjectImages
from unfold.admin import ModelAdmin, TabularInline


# عرض الصور داخل المشروع بشكل Tabular
class ProjectImagesTabular(TabularInline):  # استخدم TabularInline من unfold
    model = ProjectImages
    extra = 1  # عدد الصفوف الإضافية لصور جديدة


# إدارة مشاريع التخرج بتنسيق Unfold محسّن
@admin.register(GraduationProject)
class GraduationProjectAdmin(ModelAdmin):  # استخدم ModelAdmin من unfold

    list_display = (
        'title',
        'graduation_year',
        'category',
        'status',
        'created_at',
        'updated_at',
    )
    search_fields = ('title', 'graduation_year', 'category__name')
    list_filter = ('status', 'graduation_year', 'category')
    ordering = ('-id',)
    list_per_page = 50
    inlines = [ProjectImagesTabular]

    # تقسيم الحقول إلى أقسام منظمة داخل صفحة الإضافة/التعديل
    fieldsets = (
        ('Basic Info', {
        'fields': (
            'title', 'title_ar', 'description', 'sub_description',
            'graduation_year', 'status', 'students', 'doctor', 'supervisors',
            'category', 'book_pdf', 'images', 'video', 'audio_file',
            'likes', 'slug', 'view_count'
        ),
        }),
        ('Additional Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # تخليها قابلة للطي
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # لو الحقول دي بتتحدث تلقائيًا


# إدارة التصنيفات
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# إدارة المراجعات
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    # list_display = ('project', 'rating', 'created_at')
    search_fields = ('project__title',)
    # list_filter = ('rating', 'created_at')


# إدارة الصور بشكل مباشر (لو حابب)
# @admin.register(ProjectImages)
# class ProjectImagesAdmin(ModelAdmin):
#     # list_display = ('project', 'image', 'created_at')
#     # list_filter = ('created_at',)
