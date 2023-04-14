from django.db import models
from django.db.models import QuerySet


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
    
    def save(self, *args, **kwargs):
        if not self.isPublic:
        # Set all collections to private when the database is private
            self.collections.update(isPublic=False)
        super().save(*args, **kwargs)

    def show_collections(self, admin=False):
        if admin or self.isPublic:
            return self.collections.all()
        #return QuerySet(model=CollectionPermission).none()
        return "This database is private."
    
class CollectionPermission(models.Model):
    collection_name = models.CharField(max_length=255)
    database = models.ForeignKey(DatabasePermission, on_delete=models.CASCADE, related_name='collections')
    isPublic = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.database.isPublic:
            self.isPublic = False
        # Check if database exists, otherwise create one
        database = DatabasePermission.objects.filter(database_name=self.database.database_name).first()
        if database is None:
            database = DatabasePermission(database_name=self.database.database_name, isPublic=self.database.isPublic)
            database.save()
            self.database = database
        super(CollectionPermission, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.collection_name} in {self.database.database_name}'
    
    class Meta:
        unique_together = ('collection_name', 'database')