from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from django.shortcuts import get_object_or_404
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from .models import Job
from webdriver_manager.chrome import ChromeDriverManager

scroll_js = "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });"

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)

#### linkedin ####
def get_topInfo(page):
    """
    Get Date And Applications
    """
    soup = BeautifulSoup(page, 'html.parser')

    try:
        div_elements = soup.find_all('div', class_='topcard__flavor-row')
        text_values = [text.split('\n') for div in div_elements for text in div.stripped_strings]
        return sum(text_values, [])
    except AttributeError:
        return ["","","",""]


def clear_linkedin(all_job_link):
    print("- Clear Linkedin -")
    print(len(all_job_link))
    i = 1
    i_del = 1
    for job_link in all_job_link:
        driver.get(job_link)
        try: job = get_object_or_404( Job, job_link=f"{job_link}\n" )
        except: job = get_object_or_404( Job, job_link=f"{job_link}" )
        while True:
            sleep(randint(2, 5))
            if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
                print("HTTP ERROR 429")
                driver.refresh()
            else:
                break

        while True:
            sleep(randint(5, 10))

            if "authwall" in driver.current_url:
                sleep(randint(10, 20))
                driver.get(job_link)
                print(f"{i}) trying again, We found authwall")
            else: break

        

        sleep(randint(3, 5))
        if "Page not found" in driver.page_source:
            print(f"{i}) Page not found, Link={job_link}")
            i += 1
            sleep(randint(1, 3))
            job.delete()
            print(f"{i_del}) Deleted Job.")
            i_del += 1
            continue
        
        sleep(randint(1, 3))
        if "This job is no longer available" in driver.page_source or 'No longer accepting applications' in driver.page_source:
            job.delete()
            print(f"{i_del}) Deleted Job.")
            i_del += 1
            continue
        
        infos = get_topInfo(driver.page_source)
        if not infos[3] == "":
            job.applications = infos[3]
            print("Updating Application Count")

        if not infos[2] == '':
            job.post_date = infos[2]
            print("Updating Post Date")

        job.save()
        
        print(f"Job Available: {i}/{len(all_job_link)}), link: {job_link}")
        print(f"Job Deleted: {i_del}/{len(all_job_link)} ")
        print("------------------------------------------------")
        i += 1
#### linkedin ####



#### indeed ####
        
def clear_indeed(all_job_link):
    print("- Clear Indeed -")
    print(all_job_link)
    print(len(all_job_link))
    i = 1
    i_del = 1
    for job_link in all_job_link:
        driver.get(job_link)
        job = get_object_or_404( Job, job_link=job_link )

        while True:
            sleep(randint(2, 5))
            if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
                print("HTTP ERROR 429")
                driver.refresh()
            else:
                break
        

        sleep(randint(3, 5))
        if "Page not found" in driver.page_source:
            print(f"{i}) Page not found, Link={job_link}")
            sleep(randint(1, 3))
            job.delete()
            print(f"{i_del}) Deleted Job, Link={job_link}")
            i_del += 1
            continue
        
        sleep(randint(1, 3))
        if "This job has expired on Indeed" in driver.page_source and 'Reasons could include: the employer is not accepting applications, is not actively hiring, or is reviewing applications' in driver.page_source:
            job.delete()
            print(f"{i_del}) Deleted Job, Link={job_link}")
            i_del += 1
            continue
        
        print(f"Job Available: {i}/{len(all_job_link)}), link: {job_link}")
        print(f"Job Deleted: {i_del}/{len(all_job_link)} ")

        print("------------------------------------------------")
        i += 1

#### indeed ####

linkedin_link = []
indeed_link = []

all_jobs = Job.objects.all()
all_job_link = [job.job_link.strip() for job in all_jobs if job.job_link]

for job_link in all_job_link:
    if 'indeed.com' in job_link:
        indeed_link.append(job_link)

    elif 'linkedin.com' in job_link:
        linkedin_link.append(job_link)

    
clear_indeed(indeed_link)
clear_linkedin(linkedin_link)




