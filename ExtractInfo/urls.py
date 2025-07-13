from django.urls import path
from . import views

urlpatterns = [
    path("search_hospitals/", views.search_hospitals, name="search_hospitals"),
]
