from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('doctor', 'Doctor'),
        ('supervisor', 'Supervisor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)  # Optional for Doctor/Supervisor

    # Fixing reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='graduation_project_user_groups',  # Unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='graduation_project_user_permissions',  # Unique related_name
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Graduation Project
class GraduationProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    sub_description = models.TextField(blank=True, null=True)
    graduation_year = models.IntegerField()
    students = models.ManyToManyField(User, related_name="student_projects", limit_choices_to={'role': 'student'})
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="doctor_projects", limit_choices_to={'role': 'doctor'})
    supervisors = models.ManyToManyField(User, related_name="supervisor_projects", limit_choices_to={'role': 'supervisor'})
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="projects")
    book_pdf = models.FileField(upload_to="projects/books/", blank=True, null=True)
    images = models.ImageField(upload_to="projects/images/", blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Review
class Review(models.Model):
    project = models.ForeignKey(GraduationProject, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_reviews")
    comments = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.project.title} by {self.reviewer.username}"
