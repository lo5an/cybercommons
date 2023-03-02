from django.shortcuts import render

from api import config
from data_store.views import DataStore, DataStoreDetail, MongoDataStore

from .models import catalogModel
from .permission import CatalogPermission, createCatalogPermission


class Catalog(MongoDataStore):
    permission_classes = (createCatalogPermission,)
    connect_uri = config.CATALOG_URI
    model = catalogModel
    view_reverse = "catalog"
    exclude = config.CATALOG_EXCLUDE
    include = config.CATALOG_INCLUDE
    name = "Catalog"


class CatalogData(DataStore):
    permission_classes = (CatalogPermission,)
    model = catalogModel
    connect_uri = config.CATALOG_URI


class CatalogDataDetail(DataStoreDetail):
    permission_classes = (CatalogPermission,)
    model = catalogModel
    connect_uri = config.CATALOG_URI
