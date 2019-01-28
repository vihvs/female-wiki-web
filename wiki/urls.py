from django.urls import path

from . import views

urlpatterns = [
    path('results/', views.PageListView.as_view(), name='page-list'),
    path('search/', views.SearchView.as_view(), name='search'),
]
