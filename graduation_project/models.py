from django.contrib.auth.models import User
from django.db import models






class GraduationProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    sub_description = models.TextField(blank=True, null=True)
    graduation_year = models.IntegerField()
    # Filter out users who are doctors or teaching assistants (students can only be regular users)
    students = models.ManyToManyField(
        User,
        related_name="student_projects",
        limit_choices_to=models.Q(profile__is_doctor=False) & models.Q(profile__is_teaching_assistant=False)
    )
    # Ensure that only users who are doctors can be assigned as a doctor for the project
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="doctor_projects",
        limit_choices_to=models.Q(profile__is_doctor=True)  # Only doctors allowed
    )
    # You can add supervisors if needed (e.g., same restrictions or just users with specific roles)
    supervisors = models.ManyToManyField(
        User,
        related_name="supervisor_projects",
        blank=True  # You can adjust whether supervisors can be optional or not
    )
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
