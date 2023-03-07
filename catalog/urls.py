_author__ = 'mstacy'
from django.urls import path, re_path

from catalog.views import Catalog, CatalogData, CatalogDataDetail

urlpatterns = [
     path('data/', Catalog.as_view(),name='catalog-list'),
     re_path(r'data/(?P<database>[^/]+)/$',Catalog.as_view(),name='catalog-list'),
     re_path(r'data/(?P<database>[^/]+)/(?P<collection>[^/]+)/$',CatalogData.as_view(),name='catalog-detail'),
     re_path(r'data/(?P<database>[^/]+)/(?P<collection>[^/]+)/(?P<id>[^/]+)/$', CatalogDataDetail.as_view(),
             name='catalog-detail-id'),
]

