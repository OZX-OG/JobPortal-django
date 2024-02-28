from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scrape_linkedin", views.scrape_linkedin_jobs, name="scrape_linkedin"),
    path("scrape_indeed", views.scrape_indeed_jobs, name="scrape_indeed"),
    path("clear", views.clear_scrape, name="clear"),
    
    path("<slug:slug>", views.job_details, name="job_details"),
]