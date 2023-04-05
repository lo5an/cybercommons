from django.db import models

# Create your models here.

class dataStore(models.Model):
    class Meta:
        managed=False
        permissions = (
            ('datastore_admin', 'Data Store Admin'),
            ('datastore_create','Create DataStore Databases and Collections'),
        )
    pass

class DatabasePermission(models.Model):
    database_name = models.CharField(max_length=255)
    isPublic = models.BooleanField(default=True)
    
    def __str__(self):
        return self.database_name
class CollectionPermission(models.Model):
    collection_name = models.CharField(max_length=255)
    database = models.ForeignKey(DatabasePermission, on_delete=models.CASCADE, related_name='collections')
    isPublic = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.database.isPublic:
            self.isPublic = False
        super(CollectionPermission, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.collection_name} in {self.database.database_name}'
