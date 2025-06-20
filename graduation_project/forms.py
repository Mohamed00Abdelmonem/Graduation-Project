from django import forms
from .models import GraduationProject, User
from django.db.models import Q

class GraduationProjectForm(forms.ModelForm):
    class Meta:
        model = GraduationProject
        fields = [
            'title', 'title_ar', 'description', 'sub_description', 'graduation_year', 
            'category', 'doctor', 'students', 'supervisors', 'images', 'book_pdf', 'video'
        ]

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # عرض فقط teaching assistants في قائمة المشرفين
        self.fields['supervisors'].queryset = User.objects.filter(
            profile__is_teaching_assistant=True
        )

       # الطلاب = سنة رابعة فقط + لم يتم اختيارهم في أي مشروع قبل كده
        used_ids = list(filter(None, GraduationProject.objects.values_list('students__id', flat=True)))

        self.fields['students'].queryset = User.objects.filter(
            profile__grade='4',
            profile__is_doctor=False,
            profile__is_teaching_assistant=False
        ).exclude(id__in=used_ids)
