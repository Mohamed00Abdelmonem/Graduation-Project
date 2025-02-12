from django import forms
from .models import Experience
from .models import UserProfile
from django.forms.widgets import DateInput





class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="رفع ملف Excel")

class NationalIDLoginForm(forms.Form):
    national_id = forms.CharField(label='National ID', max_length=14, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your National ID'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'phone_number', 'grade', 'image',
            'job_title', 'whatsapp_number', 'linkedin_link', 'instgram_link', 'porfolio_link', 'short_bio', 'department', 'date_of_birth',
            'address'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].choices = [('', '---------')] + list(self.fields['grade'].choices)    






class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'company', 'from_date', 'to_date', 'position',
            'projects_worked_name', 'projects_worked_url', 'description'
        ]
        widgets = {
            'from_date': DateInput(attrs={'type': 'date'}),  # Use HTML5 date input
            'to_date': DateInput(attrs={'type': 'date'}),    # Use HTML5 date input
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if to_date and from_date and to_date < from_date:
            raise forms.ValidationError("End date must be after start date.")