# accounts/views.py
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ExcelUploadForm
from .models import UserProfile




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import NationalIDLoginForm


@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect




def national_id_login(request):
    if request.method == 'POST':
        form = NationalIDLoginForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            password = form.cleaned_data['password']

            user = authenticate(request, national_id=national_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid National ID or password'})
    else:
        form = NationalIDLoginForm()
    return render(request, 'login.html', {'form': form})





def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        
        # Debug: Log the columns in the uploaded file
        print(f"Columns in the uploaded file: {df.columns.tolist()}")

        for _, row in df.iterrows():
            name = row['name']
            national_id = row['national_id']
            username = row['username']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            phone_number = row.get('phone_number', '')
            year_grade = row.get('year_grade', '')
            is_leader = row.get('is_leader', False)
            is_doctor = row.get('is_doctor', False)
            is_teaching_assistant = row.get('is_teaching_assistant', False)
            address = row.get('address', '')

            # Creating or updating the user
            user, created = User.objects.update_or_create(
                username=first_name + last_name,  # Use first_name + last_name as the username
                defaults={'first_name': first_name, 'last_name': last_name, 'email': email}
            )
            if created:
                user.set_password(str(national_id))  # Convert national_id to string before setting as password
                user.save()

                # Create or update the profile with national_id
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'national_id': national_id,  # Save the national_id in the UserProfile
                        'phone_number': phone_number,
                        'year_grade': year_grade,
                        'is_leader': is_leader,
                        'is_doctor': is_doctor,
                        'is_teaching_assistant': is_teaching_assistant,
                        'address': address
                    }
                )
        
        return render(request, 'upload_success.html')

    return render(request, 'upload_form.html', {'form': ExcelUploadForm()})
