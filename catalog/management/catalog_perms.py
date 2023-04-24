from django.core.management.base import BaseCommand, CommandError
from catalog.models import Catalog_DatabasePermission, Catalog_CollectionPermission
from api import config
from celery import Celery
from bson import ObjectId
from bson.errors import InvalidId


class celeryConfig:
    BROKER_URL = config.BROKER_URL
    BROKER_USE_SSL = config.BROKER_USE_SSL
    CELERY_SEND_EVENTS = True
    CELERY_TASK_RESULT_EXPIRES = None
    CELERY_RESULT_BACKEND = config.CELERY_RESULT_BACKEND
    CELERY_MONGODB_BACKEND_SETTINGS = config.CELERY_MONGODB_BACKEND_SETTINGS

app = Celery()
app.config_from_object(celeryConfig)

class Command(BaseCommand):
    help = "Imports Mongo Database and Collection into Django Permissions"

    def handle(self, *args, **options):
        db = app.backend.database.client
        for database in db.list_database_names():
            if database not in config.CATALOG_EXCLUDE:
                dbPerm = Catalog_DatabasePermission.objects.filter(database_name=database).first()
                if dbPerm is None:
                    dbPerm = Catalog_DatabasePermission(database_name=database)
                    dbPerm.save()
                for collection in db[database].list_collection_names():
                    if collection not in config.CATALOG_EXCLUDE:
                        colPerm = Catalog_CollectionPermission.objects.filter(collection_name=collection).first()
                        if colPerm is None:
                            colPerm = Catalog_CollectionPermission(collection_name=collection, database=dbPerm)
                            colPerm.save()