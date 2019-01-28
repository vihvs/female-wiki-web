from django.urls import path

from . import views

urlpatterns = [
    path('results/', views.PageListView.as_view(), name='page-list'),
]
