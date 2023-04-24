from django.db import models
from django.contrib.auth.models import User
from data_store.models import DatabasePermission, CollectionPermission
# Create your models here.

class catalogModel(models.Model):
    class Meta:
        managed=False
        permissions = (
            ('catalog_admin', 'Catalog Admin'),
            ('catalog_create','Create Catalog Collections'),
        )

class Catalog_DatabasePermission(DatabasePermission):
    pass

class Catalog_CollectionPermission(CollectionPermission):
    pass
