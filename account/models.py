from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)


class Categories(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="categories")

    title = models.CharField(max_length=100)


class Tasks(models.Model):
    category = models.ForeignKey(Categories, models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)