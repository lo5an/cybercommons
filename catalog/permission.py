from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from api import config
from data_store.permission import DataStorePermission

# class CatalogPermission(permissions.BasePermission):
#     """
#     DataStore Detail View Permissions.
#     SAFE_METHODS always TRUE
#     UNSAFE need appropriate Permissions
#     """
#     def __init__(self,anonymous=config.CATALOG_ANONYMOUS):
#         self.anonymous = anonymous
#     def has_permission(self, request, view):

#         django_app = 'catalog'
#         admin_perm = 'catalog.catalog_admin'
#         path = request.path.split('/')
#         database = path[path.index(django_app)+2]
#         collection = path[path.index(django_app)+3]
#         perms=list(request.user.get_all_permissions())
#         if request.method in permissions.SAFE_METHODS:
#             code_perm= "{0}.{1}_{2}_{3}".format(django_app,database,collection,'safe')
#             #print perms, admin_perm,code_perm
#             if self.anonymous or admin_perm in perms or code_perm in perms:
#                 return True
#             else:
#                 return False
#         else:
#             code_perm= "{0}.{1}_{2}_{3}".format(django_app,database,collection,request.method.lower())
#             if request.user.is_superuser or admin_perm in perms or code_perm in perms:
#                 return True
#             else:
#                 return False

class CatalogPermission(DataStorePermission):
    """
    A custom permission class for Catalog app. Inherits from DataStorePermission
    and sets the required permissions for catalog application.
    
    :ivar django_app: A string representing the name of the Django app for which permissions are to be set
    :ivar admin_perm: A string representing the name of the permission required for administrative access
    :ivar view_perm: A string representing the name of the permission required for viewing Catalog models
    """
    django_app = 'catalog'
    admin_perm = 'catalog.catalog_admin'
    view_perm = 'catalog.view_catalogmodel'
    
class createCatalogPermission(permissions.BasePermission):
    """
    A custom permission class to allow creation of databases and collections.
    Inherits from BasePermission and provides the logic to check if the user has the required
    permissions to create new Catalog objects.
    
    :ivar has_permission: A method to check if the user has permission to create Catalog objects.
    """
    
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            django_app = 'catalog'
            admin_perm = 'catalog.catalog_admin'
            #Control catalog names per api_config
            path=request.path.split('/')
            if len(path)-(path.index(django_app))==3:
                return False 
            perms=list(request.user.get_all_permissions())
            if request.user.is_superuser or admin_perm in perms: #or code_perm in perms:
                return True
            else:
                return False

