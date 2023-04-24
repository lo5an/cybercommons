from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# Register your models here.
from api import config
from .models import catalogModel, Catalog_DatabasePermission, Catalog_CollectionPermission
#from pymongo import MongoClient
from celery import Celery
from data_store.admin import DatabasePermissionAdmin, CollectionPermissionAdmin

class celeryConfig:
    BROKER_URL = config.BROKER_URL
    BROKER_USE_SSL = config.BROKER_USE_SSL
    CELERY_SEND_EVENTS = True
    CELERY_TASK_RESULT_EXPIRES = None
    CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND
    CELERY_MONGODB_BACKEND_SETTINGS = config.CELERY_MONGODB_BACKEND_SETTINGS


app = Celery()
app.config_from_object(celeryConfig)


def setpermissions(app_label,codename,name):
    ct = ContentType.objects.get_for_model(catalogModel)
    #ct=ContentType.objects.get(app_label=app_label)
    Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)

#Catalog Permissions
#db = MongoClient(host=config.CATALOG_URI)
db = app.backend.database.client
for catalog in config.CATALOG_INCLUDE:
    for col in db[catalog].list_collection_names():
        if not (col in config.CATALOG_EXCLUDE):
            for method in [('post','ADD'),('put','UPDATE'),('delete','DELETE'),('safe','SAFE METHODS')]:
                codename= "{0}_{1}_{2}".format(catalog,col,method[0])
                name = "{0} {1} {2}".format(catalog,col,method[1])
                setpermissions('catalog',codename,name)

#Create Admin Permissions
setpermissions('catalog','catalog_admin','Catalog Admin')

class Catalog_DatabasePermissionAdmin(DatabasePermissionAdmin):
    pass

class Catalog_CollectionPermissionAdmin(CollectionPermissionAdmin):
    pass

admin.site.register(Catalog_DatabasePermission, Catalog_DatabasePermissionAdmin)
admin.site.register(Catalog_CollectionPermission, Catalog_CollectionPermissionAdmin)