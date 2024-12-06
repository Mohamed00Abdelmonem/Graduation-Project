# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

Year_Grade = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('not_student', 'Not a Student'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    national_id = models.CharField(max_length=20, unique=True)  # Add National ID field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    year_grade = models.CharField(max_length=20, choices=Year_Grade, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_leader = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_teaching_assistant = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
        

    def __str__(self):
        return f"{self.user.username} Profile"

   