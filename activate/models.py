from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class ActivateLog(models.Model):
    user = models.ForeignKey(User, related_name='activate_user', on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=500)
    browser_name = models.CharField(max_length=100, null=True, blank=True)  # جديد
    status = models.CharField(max_length=20, null=True, blank=True)  # جديد
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.method} - {self.url} - {self.created_at}"
