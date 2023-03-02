__author__ = "mstacy"
from django.conf.urls import url
from django.urls import include, path, re_path

# from rest_framework.urlpatterns import format_suffix_patterns
from api import config
from data_store.views import DataStore, DataStoreDetail, MongoDataStore

urlpatterns = [
    path("data/", MongoDataStore.as_view(), name="data-list"),
    re_path(r"data/(?P<database>[^/]+)/$", MongoDataStore.as_view(), name="data-list"),
    re_path(
        r"data/(?P<database>[^/]+)/(?P<collection>[^/]+)/$",
        DataStore.as_view(),
        name="data-detail",
    ),
    re_path(
        r"data/(?P<database>[^/]+)/(?P<collection>[^/]+)/(?P<id>[^/]+)/$",
        DataStoreDetail.as_view(),
        name="data-detail-id",
    ),
]


# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
