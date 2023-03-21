__author__ = 'mstacy'
from django.urls import path, re_path
from data_store.views import MongoDataStore, DataStore, DataStoreDetail

urlpatterns = [
    path('data/', MongoDataStore.as_view(), name='data-list'),
    re_path(r'data/(?P<database>[^/]+)/$', MongoDataStore.as_view(), name='data-list'),
    re_path(r'data/(?P<database>[^/]+)/(?P<collection>[^/]+)/$', DataStore.as_view(),name='data-detail'),
    re_path(r'data/(?P<database>[^/]+)/(?P<collection>[^/]+)/(?P<id>[^/]+)/$', DataStoreDetail.as_view(),
                           name='data-detail-id'),
]

