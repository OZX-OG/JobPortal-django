from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_token.as_view(), name="api_token"),
    path("random/", views.api, name="api"),
    
]