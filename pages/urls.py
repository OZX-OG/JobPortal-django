from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scrape", views.scrapee, name="scrape"),
    path("clear", views.clear_scrape, name="clear_scrape"),
    
    path("<slug:slug>", views.job_details, name="job_details"),
]