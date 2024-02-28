from celery import shared_task
from pages.scrape_indeed import main as indeed_main
from pages.scrape_linkedin import main as linkedin_main
from pages.clear_scrape import main as clear_jobs

@shared_task
def scrape_linkedin():
    return linkedin_main()

@shared_task
def scrape_indeed():
    return indeed_main()

@shared_task
def clear_jobs_fromDB():
    return clear_jobs