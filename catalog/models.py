from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class catalogModel(models.Model):
    class Meta:
        managed=False
        permissions = (
            ('catalog_admin', 'Catalog Admin'),
            ('catalog_create','Create Catalog Collections'),
        )

class Catalog_DatabasePermission(models.Model):
    """
    A Django model representing permission to access a database.

    :ivar database_name: A CharField representing the name of the database.
    :ivar isPublic: A BooleanField representing whether the database is public or private.
    """
    
    database_name = models.CharField(max_length=255)
    isPublic = models.BooleanField(default=True)
    
    def __str__(self):
        return self.database_name
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to set all collections to private when the database is set to private.
        """
        
        if not self.isPublic:
        # Set all collections to private when the database is private
            self.collections.update(isPublic=False)
        super().save(*args, **kwargs)

    def show_collections(self, admin=False):
        """
        Returns a queryset of CollectionPermission objects related to this database if the database is public,
        and a string message otherwise.

        :param admin: A boolean indicating if the user is an admin.
        :return: A QuerySet of CollectionPermission objects or a string message.
        """
        
        if admin or self.isPublic:
            return self.collections.all()
        #return QuerySet(model=CollectionPermission).none()
        return "This database is private."
    
class Catalog_CollectionPermission(models.Model):
    """
    A Django model representing permission to access a collection.

    :ivar collection_name: A CharField representing the name of the collection.
    :ivar database: A ForeignKey representing the related database.
    :ivar isPublic: A BooleanField representing whether the collection is public or private.
    """
    
    collection_name = models.CharField(max_length=255)
    database = models.ForeignKey(Catalog_DatabasePermission, on_delete=models.CASCADE, related_name='collections')
    isPublic = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the collection to private if the database is private, and to create the
        related database if it does not exist.
        """
        
        if not self.database.isPublic:
            self.isPublic = False
        # Check if database exists, otherwise create one
        database = Catalog_DatabasePermission.objects.filter(database_name=self.database.database_name).first()
        if database is None:
            database = Catalog_DatabasePermission(database_name=self.database.database_name, isPublic=self.database.isPublic)
            database.save()
            self.database = database
        super(Catalog_CollectionPermission, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.collection_name} in {self.database.database_name}'
    
    class Meta:
        unique_together = ('collection_name', 'database')