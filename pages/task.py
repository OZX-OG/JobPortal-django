from celery import shared_task
from pages.scrape_indeed import main as indeed_main
from pages.scrape_linkedin import main as linkedin_main

@shared_task
def scrape_and_update_jobs():
    # return indeed_main()
    return linkedin_main()


@shared_task
def clear_jobs_fromDB():
    import pages.clear_scrape
    return 'salam'
