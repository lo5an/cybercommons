from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class taskModel(models.Model):
    class Meta:
        managed = False
        permissions = (("task_admin", "Task Admin"),)
