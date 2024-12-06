from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="رفع ملف Excel")

from django import forms

class NationalIDLoginForm(forms.Form):
    national_id = forms.CharField(label='National ID', max_length=14, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your National ID'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))