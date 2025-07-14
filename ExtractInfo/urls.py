from django.urls import path
from . import views

urlpatterns = [
    path("extract_data/", views.extract_data, name="extract_data"),
    path("transform_data/", views.transform_data, name="transform_data"),
]
