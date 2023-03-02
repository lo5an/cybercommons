from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class catalogModel(models.Model):
    class Meta:
        managed = False
        permissions = (
            ("catalog_admin", "Catalog Admin"),
            ("catalog_create", "Create Catalog Collections"),
        )
