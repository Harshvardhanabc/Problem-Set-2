from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

class App(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    logo_url = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

