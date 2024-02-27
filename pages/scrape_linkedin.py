print("bsmlah")
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
from .models import Job, Location, Source, Scrape

scroll_js = "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });"
country_locations = ['Germany', 'spain', 'United States', 'portugal', 'United Kingdom', 'france', 'United Arab Emirates', 'russia']
SOURCE = 'Linkedin'
scrape_index = Scrape.objects.get(id=1)
remote = '&f_WT=2' 

# url = 'https://www.linkedin.com/jobs/search?keywords=Django&location=Worldwide&geoId=92000000&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        
options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
options.add_argument('--headless')
driver_path = 'C:/Program Files (x86)/chromedriver.exe'
driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=options)

# url = f'https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords=django&location={ country_locations[scrape_index.loc_linkedin_indx] }{remote}'
# driver.get(url)

"""
celery -A JobPortal worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
"""

def click_button_showMore(driver):
    more_btn = "infinite-scroller__show-more-button--visible"
    button_elements = driver.find_elements(By.CLASS_NAME, more_btn)
    if len(button_elements) > 0:
        sleep(randint(1,3))
        driver.find_element(By.CLASS_NAME, more_btn).click()
        print("Clicked")

def is_the_end(driver, i, url):
    try:
        driver.find_element(By.CSS_SELECTOR, "#main-content > section.two-pane-serp-page__results-list > div.px-1\.5.flex.inline-notification.hidden.text-color-signal-positive.see-more-jobs__viewed-all")
        print(f"{i}) Still Scrolling. link={driver.current_url}")
        if i % 10 == 0:
            print(len(driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/section[2]/ul/li")))            
        return True
    except Exception as e:
        if "authwall" in driver.current_url:
            i = 1
            while True:
                if "authwall" in driver.current_url:
                    sleep(randint(10, 20))
                    driver.get(url)
                    print(f"{i}) trying again, We found authwall")
                    i += 1
                else:
                    return True
        else:
            print(f"Ending... || {e}")
            return False

def get_links(r = True):
    ## Scroll to max job to load all jobs on the page
    remote = '&f_WT=2' if r else ''
    url = f'https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords=django&location={ country_locations[scrape_index.loc_linkedin_indx] }{remote}'
    driver.get(url)

    sleep(randint(1,3))
    if 'We couldn’t find a match for' in driver.page_source:
        print("No Job Appear.")
        return []
    
    loop = 1
    while is_the_end(driver, loop, url):
        sleep(randint(1,3))
        
        if loop == 10: print(scroll_js)
        driver.execute_script(scroll_js)
        click_button_showMore(driver)
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/ul/li[1000]")
            break
        except:
            pass

        sleep(randint(1,3))
        loop += 1
    
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a_hrefs = soup.find_all("a")

    all_job_link = []
    for a_href in a_hrefs:
        href = a_href.get("href")
        if href == None: continue
        if "jobs/view" in href:
            href = href.split(".")
            href.pop(0)
            href = f"https://{'.'.join(href)}".split('?')[0]
            all_job_link.append(href)
            print(f"{country_locations[scrape_index.loc_linkedin_indx].lower()} - {href}")
    
    return all_job_link

# getjobs()




def get_company_url(soup):
    a_element = soup.find('a', class_='topcard__org-name-link topcard__flavor--black-link')
    try: return a_element.get('href')
    except AttributeError: return None

def get_descriptions(soup):
    div_element = soup.find('div', class_='show-more-less-html__markup')
    content_html = div_element.encode_contents().decode()
    return content_html

def get_imag_url(soup):
    try:
        # Find the img element with the specified class
        img_element = soup.find('img', class_='sub-nav-cta__image')
        # Extract the value of the data-delayed-url attribute
        data_delayed_url = img_element.get('data-delayed-url', 'link not found')
        if data_delayed_url == "link not found":
            return img_element.get('src', 'link not found')
        
        return data_delayed_url
    except AttributeError:
        return "link not found"
    
def get_topInfo(soup):
    try:
        div_elements = soup.find_all('div', class_='topcard__flavor-row')
        text_values = [text.split('\n') for div in div_elements for text in div.stripped_strings]
        return sum(text_values, [])
    except AttributeError:
        return ["","","",""]

def get_lowerInfo(soup):
    # try:
    res = {}
    ul_element = soup.find('ul', class_='description__job-criteria-list')
    # ul_content = ul_element.get_text(separator='\n').strip()
    span_values = [span.get_text(strip=True) for span in ul_element.find_all('span', class_='description__job-criteria-text--criteria')]
    h3_values = [h3.get_text(strip=True) for h3 in ul_element.find_all('h3', class_='description__job-criteria-subheader')]
    for i in range(len(h3_values)):
        res[ h3_values[i].lower().replace(" ", "_") ] = span_values[i]

    return res
        # return span_values, h3_values 
    # except AttributeError:
    #     print(res) 
    #     return {'seniority_level': '-', 'employment_type': '-', 'industries': '-', }

def get_title(soup):
    try:
        title_h1 = soup.find('h1', class_='top-card-layout__title')
        title = title_h1.get_text(strip=True)
        return title
    except AttributeError:
        return "Not found"


def get_price(soup):
    compensation_div = soup.find('div', class_='compensation__salary-range')
    salary_range = "Not specified"

    if compensation_div:
        salary_range = compensation_div.find('div', class_='compensation__salary').get_text(strip=True)

    return salary_range

# f= open("txt1.txt", 'r')
# all_job_link = f.readlines()
# f.close()

def get_job(all_job_link):
    print(len(all_job_link))
    print("------------------------------------------------")
    i = 1
    for job_link in all_job_link:
        if not Job.objects.filter( job_link=job_link ).exists():
            driver.execute_script("window.open('about:blank', '_blank');")
            
            new_window_handle = driver.window_handles[-1]
            driver.switch_to.window(new_window_handle)
            
            driver.get(job_link)

            while True:
                sleep(randint(5, 10))

                if "authwall" in driver.current_url:
                    sleep(randint(10, 20))
                    if randint(0, 10) % 2 == 0 :
                        pass
                    driver.get(job_link)
                    print(f"{i}) trying again, We found authwall")
                else: break

            sleep(randint(3, 5))
            if "Page not found" in driver.page_source:
                print(f"{i}) Page not found, Link={job_link}")
                i += 1
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                sleep(randint(1, 3))
                continue

            while True:
                sleep(randint(2, 5))
                if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
                    print("HTTP ERROR 429")
                    driver.refresh()
                else:
                    break
            
            if randint(0, 10) % 2 == 0 :
                driver.execute_script(scroll_js)

            sleep(randint(1, 3))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            print("------------------------------------------------")
            titleJob = get_title(soup)
            TopInfo = get_topInfo(soup)
            infos = get_lowerInfo(soup)
            image = get_imag_url(soup)
            cmp_url = get_company_url(soup)
            salary= get_price(soup)
            print(titleJob)
            print(job_link)
            print(salary)
            print(TopInfo)
            print(infos)
            print(image)
            print(cmp_url)
            
            descr = get_descriptions(soup)
            # Source.objects.get_or_create(source=SOURCE)
            # Location.objects.get_or_create(location=TopInfo[1])
            source_obj, _ = Source.objects.get_or_create(source=SOURCE)
            location_obj, _ = Location.objects.get_or_create(location = country_locations[scrape_index.loc_linkedin_indx].lower() )

            job = Job.objects.create(
                title = titleJob.strip(),
                company=TopInfo[0].strip(),

                description = descr.strip(), 
                
                job_link = job_link.strip(),
                company_url = cmp_url.strip(),
                image_url = image.strip(),

                salary = salary,

                specific_location = TopInfo[1].strip(),

                # source = SOURCE,
                # locations = TopInfo[1],

                applications = TopInfo[3],
                seniority_level = infos['seniority_level'],
                employment_type = infos['employment_type'],
                Industries = infos['industries'],
                post_date = TopInfo[2],
            
                remote = False
            )

            job.location.add(location_obj)
            job.source.add(source_obj)
            job.save()

            print("Added Successfully")
        
        
            print(f"Job Number {i}/{len(all_job_link)} done, Link: {job_link}")
            print("------------------------------------------------")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            sleep(randint(3, 5))
        else:
            print("Not Added, Is already Exist")
            print(f"{i}) Link: {job_link}")
            print("------------------------------------------------")
            
        i += 1
    

def remote(all_job_link):
    for indx, job_link in enumerate(all_job_link):
        if Job.objects.filter( job_link=job_link ).exists():
            job = Job.objects.get( job_link=job_link )
            job.remote = True
            job.save()
            print(f"{indx + 1}) Remote Job. Link: {job_link}")
            print("------------------------------------------------")

def main():
    for i in range(2):
        if i == 0: 
            print("Remote Off")
            all_job = get_links(False)
            
            if all_job == []:
                print("No job")
                break

            get_job(all_job)
        elif i == 1: 
            print("Remote On")
            all_job = get_links()
            
            if all_job == []:
                print("No Remote job")
                break

            remote(all_job)


    if scrape_index.loc_linkedin_indx < len(country_locations) - 1: scrape_index.loc_linkedin_indx += 1
    else: scrape_index.loc_linkedin_indx = 0
    scrape_index.save()
    driver.quit()
















# driver.quit()