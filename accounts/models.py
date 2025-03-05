from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Choices for Year/Grade
Year_Grade = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('not_student', 'Not a Student'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)  # National ID field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    grade = models.CharField(max_length=20, choices=Year_Grade, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_leader = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_teaching_assistant = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)

    porfolio_link = models.URLField(blank=True, null=True, verbose_name="Porfolio Link")  # Porfolio Link
    linkedin_link = models.URLField(blank=True, null=True, verbose_name="LinkedIn Link")  # LinkedIn Link
    instgram_link = models.URLField(blank=True, null=True, verbose_name="instagram Link")  # instagram Link
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم واتساب")  # WhatsApp Number
    job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="المسمي الوظيفي")  # Job Title
    short_bio = models.TextField(blank=True, null=True, verbose_name="نبذه مختصره عنه")  # Short Bio
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="الشعبه")  # Department


    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user = instance
        )



class Experience(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    company = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=255)
    projects_worked_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    projects_worked_url = models.URLField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.company} ({self.position})"

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-from_date']  # Order experiences by the most recent first
