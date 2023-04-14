from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from api import config
from .models import DatabasePermission, CollectionPermission

# FIXME: confirm this is dead code
# class dataStorePermission(permissions.BasePermission):
#     """
#     DataStore list API View permission.
#     SAFE_METHODS always TRUE
#     UNSAFE need appropriate Permissions
#     """
#     def __init__(self,anonymous=config.DATA_STORE_ANONYMOUS):
#         self.anonymous = anonymous
#     def has_permission(self, request, view):
#         perms=list(request.user.get_all_permissions())
#         if request.method in permissions.SAFE_METHODS:
            
#             if self.anonymous or code_perm in perms:
#                 return True
#             else:
#                 return False
#         else:
#             django_app = 'data_store'
#             admin_perm = 'data_store.datastore_admin'
#             path = request.path
#             path=path.split('/')
#             code_perm= "{0}.{1}_{2}_{3}".format(django_app,request.method.lower(), path[-3],path[-2])
#             if request.user.is_superuser or admin_perm in perms or code_perm in perms:
#                 return True
#             else:
#                 return False 

class createDataStorePermission(permissions.BasePermission):
    """
    DataStore create Database and Collections.
    SAFE_METHODS always TRUE
    UNSAFE need to be superuser or datastore_admin  Permissions
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            django_app = 'data_store'
            admin_perm = 'data_store.datastore_admin'
            perms=list(request.user.get_all_permissions())
            if request.user.is_superuser or admin_perm in perms:
                return True
            else:
                return False

class DataStorePermission(permissions.BasePermission):
    """
    DataStore Detail View Permissions.
    SAFE_METHODS always TRUE
    UNSAFE need appropriate Permissions
    """
    def __init__(self,anonymous=config.DATA_STORE_ANONYMOUS,read_perm_required=config.SAFE_METHOD_PERM_REQUIRED):
        self.anonymous = anonymous
        self.read_perm_required = read_perm_required

    def has_permission(self, request, view):
        django_app = 'data_store'
        admin_perm = 'data_store.datastore_admin'
        database = view.kwargs['database']
        collection = view.kwargs['collection'] 
        
        database_permission = DatabasePermission.objects.filter(database_name=database).first()
        collection_permission = CollectionPermission.objects.filter(collection_name=collection).first()
        
        perms=list(request.user.get_all_permissions())
        if request.method in permissions.SAFE_METHODS:
            if database:
                permission = collection_permission if collection else database_permission
            if admin_perm in perms or (permission and permission.isPublic):
                return True
            else:
                return False 
        else:
            code_perm= "{0}.{1}.{2}_{3}".format(django_app,database,collection,request.method.lower())
            if request.user.is_superuser or admin_perm in perms or code_perm in perms:
                return True
            else:
                return False
