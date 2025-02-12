import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import NationalIDLoginForm, UserProfileForm, ExcelUploadForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Experience
from .forms import ExperienceForm  # You'll need to create this form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Experience
from .forms import ExperienceForm  # Ensure this form exists
from graduation_project.models import GraduationProject




# ___________________________________________________________________________________


@login_required
def home(request):
    return render(request, 'logout.html', {'user': request.user})

# ___________________________________________________________________________________


def national_id_login(request):
    if request.method == 'POST':
        form = NationalIDLoginForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            password = form.cleaned_data['password']

            user = authenticate(request, national_id=national_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid National ID or password'})
    else:
        form = NationalIDLoginForm()
    return render(request, 'login.html', {'form': form})

# ___________________________________________________________________________________



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


# ___________________________________________________________________________________




@login_required
def Profile(request):
    user = request.user
        # Combine student projects and authored projects
    projects = (
        user.student_projects.all()
        | user.author_project.all()  # Union of the two querysets
    ).distinct()  # Use distinct to avoid duplicates

    return render(request, 'profile.html', {"user":user, "projects":projects})

# ___________________________________________________________________________________



@login_required
def edit_profile(request):
    user_profile = request.user.profile  # Get the current user's profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})


# ___________________________________________________________________________________




@login_required
def add_experience(request):
    if request.method == 'POST':
        # Process the form submission
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = request.user.profile  # Associate with the current user's profile
            experience.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        # Initialize an empty form
        form = ExperienceForm()

    return render(request, 'add_experience.html', {'form': form})

# ___________________________________________________________________________________



@login_required
def update_experience(request, experience_id):
    # Get the specific experience or return a 404 error if not found
    experience = get_object_or_404(Experience, id=experience_id, profile=request.user.profile)

    if request.method == 'POST':
        # Process the form submission
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        # Initialize the form with the current experience data
        form = ExperienceForm(instance=experience)

    return render(request, 'update_experience.html', {'form': form, 'experience': experience})


# ___________________________________________________________________________________



@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, profile=request.user.profile)
    experience.delete()
    return redirect('profile')


# ___________________________________________________________________________________
