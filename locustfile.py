
# This File for stress test my system using locust
import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from locust import HttpUser, task, between

class TestUser(HttpUser):
    # Define the wait time between tasks (in seconds)
    wait_time = between(1, 5)

     # Task to test the homepage
    @task
    def TestUser(self):
        self.client.get("/")
