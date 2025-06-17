from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from gtts import gTTS
import os
from django.core.files.base import ContentFile
from io import BytesIO
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
import pyttsx3
from googletrans import Translator
import os


from datetime import datetime
User = get_user_model()


# ___________________________________________________________________________________


def text_to_speech_arabic_to_english(arabic_text, instance):
    try:
        translator = Translator()
        translated = translator.translate(arabic_text, src='ar', dest='en')
        english_text = translated.text
        print("Translated text:", english_text)
    except Exception as e:
        print("Translation failed:", e)
        english_text = arabic_text  # استخدم النص الأصلي كبديل أو تجاهل

    # تابع الباقي بشكل عادي
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        selected_voice = None
        for voice in voices:
            if "english" in voice.name.lower() and ("male" in voice.name.lower() or "male" in voice.id.lower()):
                selected_voice = voice.id
                break
        if not selected_voice:
            selected_voice = voices[0].id
        engine.setProperty('voice', selected_voice)
        engine.setProperty('rate', 150)

        temp_audio_path = f"temp_audio_{instance.pk}.mp3"
        engine.save_to_file(english_text, temp_audio_path)
        engine.runAndWait()

        with open(temp_audio_path, 'rb') as f:
            instance.audio_file.save(f"audio_{instance.pk}.mp3", ContentFile(f.read()), save=False)
        os.remove(temp_audio_path)
        instance.save(update_fields=['audio_file'])

    except Exception as e:
        print("Audio generation failed:", e)


STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('temporary_rejection', 'Temporary_Rejection'),
    ]



# Get the current year
current_year = datetime.now().year

# Generate the Graduation_Year list dynamically
Graduation_Year = [(str(year), str(year)) for year in range(2010, current_year + 1)]


class GraduationProject(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, related_name="author_project")
    title = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
    description = models.TextField()
    sub_description = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to="projects/audio/", blank=True, null=True)
    graduation_year = models.CharField(
        max_length=4,  # Year is a 4-digit number
        choices=Graduation_Year,
        default=str(current_year)  # Set the default to the current year
    )    

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True  # Add this line to create an index
    )

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
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes_project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)  # Added field
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=250)


    def get_absolute_url(self):
        # استخدم slug بدلاً من id
        return reverse('project:project_detail', args=[self.slug])
    
    

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)  # حفظ عشان يبقى فيه pk

        if self.sub_description and not self.audio_file:
            # تحويل النص العربي إلى صوت إنجليزي بصوت ذكر
            text_to_speech_arabic_to_english(self.sub_description, self)

# ___________________________________________________________________________________



class ProjectImages(models.Model):
    project = models.ForeignKey(GraduationProject, related_name='project_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.project)  
    
    

# ___________________________________________________________________________________



# Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ___________________________________________________________________________________



# Review
class Review(models.Model):
    project = models.ForeignKey(GraduationProject, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_reviews")
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.project.title} by {self.reviewer.username}"


# ___________________________________________________________________________________
