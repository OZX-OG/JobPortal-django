from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
from .models import Job, Location, Source, Scrape
from webdriver_manager.chrome import ChromeDriverManager

scroll_js = "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });"
country_locations = {'United States':'www', 'Germany':'de', 'spain':'es', 'United Kingdom':'uk', 'portugal':'pt', 'france':'fr', 'United Arab Emirates':'ae'}
country = list(country_locations.items())
SOURCE = 'Indeed'
scrape_index = Scrape.objects.get(id=1)
url = f'https://www.indeed.com/jobs?q=django&start=0'

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
options.add_argument('--headless')

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)
# driver.get(url)
    
"""
https://www.indeed.com/jobs?q=django&sc=0kf%3Aattr%28DSQF7%29%3B&fromage=1

https://www.indeed.com/jobs?q=django&fromage=1
"""
# page 1 / start=0 / 15 job
# page 2 / start=10 / 30 job
# page 6 / start=50 / 90 job
# page 7 / start=60 / 105 job
# page 29/ start=280 / 435 job

def check_429():
    if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
        print("HTTP ERROR 429")
        driver.refresh()
        sleep(randint(2, 5))
        return True
    else:
        return False
    
def get_links(r = True):   
    all_job_link = []

    start = 0
    jobnum = 1
    next = True # should be True
    remote = '&sc=0kf%3Aattr%28DSQF7%29%3B' if r else ''
    while next:
        url = f'https://{country[scrape_index.loc_indeed_indx][1]}.indeed.com/jobs?q=django&fromage=1&start={start}{remote}'
        driver.get(url)
        
        driver.implicitly_wait(randint(8, 10))


        while True:
            if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
                print("HTTP ERROR 429")
                driver.refresh()
                sleep(randint(2, 5))
            else:
                break

        if 'did not match any jobs.' in driver.page_source \
            or 'Es wurden keine Jobs für die Suche' in driver.page_source \
            or 'não devolveu nenhum' in driver.page_source \
            or 'ne donne aucun résultat.' in driver.page_source \
            or 'no ha producido ningún' in driver.page_source:

            print("No Job Appear.")
            return []
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        a_hrefs = soup.find_all("a")

        # print(a_hrefs)
        data_test_ids = []
        for a_href in a_hrefs:
            href = a_href.get("href")
            if "/rc/clk?" in href:
                href = href.split("&")[0].replace("rc/clk", 'viewjob')
                link = f"https://www.indeed.com{href}"
                all_job_link.append(link)
                print(f"{jobnum}) {country[scrape_index.loc_indeed_indx][1]} - {link}")
                jobnum += 1
                continue

            if a_href.has_attr('data-testid'):
                data_test_ids.append(a_href['data-testid'])

        next = False
        # print(data_test_ids)
        if "pagination-page-next" in data_test_ids:
            next = True

        # print(f"Next: {next}")
        start += 10
        sleep(randint(2, 3))
        # break
    
    return all_job_link

# with open("selenium indeed/testjob.txt", 'w') as f:
#     for job_link in all_job_link:
#         f.write(f"{job_link}\n")

# with open("txt2.txt", 'r') as f:
#     all_job_link = f.readlines()

# print(all_job_link)
# print(all_job_link)



###### go throw job details
def get_descriptions(soup):
    div_element = soup.find('div', id='jobDescriptionText')
    content_html = div_element.encode_contents().decode()
    return content_html
    ##jobDescriptionText

def location(soup):
    try: return soup.select_one("#jobLocationText > div > span").text
    except AttributeError: return country[scrape_index.loc_indeed_indx][0]

def get_job_details(driver):
    res = {'salary': "Not specified", 'employment_type': 'Not specified'}

    jop_xpath = f'//*[@id="jobDetailsSection"]/div[1]'

    try: location_element = driver.find_element(By.XPATH, jop_xpath)
    except: return res

    location_element = driver.find_elements(By.XPATH, f'//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div/div')
    for element in location_element:
        title = element.find_element(By.CSS_SELECTOR, 'h3.js-match-insights-provider-11n8e9a').text
        curent = element.find_element(By.CSS_SELECTOR, 'div.js-match-insights-provider-tvvxwd').text
        if title.lower() == 'pay':
            title = "salary"
        elif title.lower() == 'job type':
            title = "employment_type"
    
        res[title] = curent
        
    return res

def get_job_title(soup):
    return soup.select_one("#viewJobSSRRoot > div > div.css-1quav7f.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-u4y1in.eu4oa1w0 >\
                            div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-zt53js.eu4oa1w0 >\
                            div:nth-child(1) > div.jobsearch-JobInfoHeader-title-container.css-bbq8li.eu4oa1w0 > h1 > span").text
def get_cmp_image(soup):
    data_delayed_url = ''

    for _ in range(2):
        if _ == 0:
            # Find the img element with the specified class
            img_element = soup.select_one('#cmp-container > div > div.dd-privacy-allow.css-1xyb2q9.eu4oa1w0 > header > div.css-14x0tgq.eu4oa1w0 > div.css-u74ql7.eu4oa1w0 >\
                                        div > div > div > div.css-1i5bjam.eu4oa1w0 > div.css-cfhwfm.eu4oa1w0 > div.css-bitz2j.eu4oa1w0 > div > div > img')
        else: 
            # Find the img element with the specified class
            img_element = soup.select_one('#cmp-container > div > div.dd-privacy-allow.css-1xyb2q9.eu4oa1w0 > header > div.css-14x0tgq.eu4oa1w0 > div.css-u74ql7.eu4oa1w0 >\
                                           div > div > div > div.css-122dkmk.eu4oa1w0 > div.css-cfhwfm.eu4oa1w0 > div.css-bitz2j.eu4oa1w0 > div > div > img')
            
        
        try: data_delayed_url = img_element.get('src'); break
        except AttributeError:  ...

    
    if '/cmp/-/s/' in data_delayed_url:
        return "https://indeed.com" + data_delayed_url

    return data_delayed_url
def get_cmp(so, driver):
    for _ in range(2):
        if _ == 0:
            cmp = so.find('a', class_='css-775knl')
        else:
            cmp = so.find('a', class_='css-1cxc9zk')

        try: cmp_name = cmp.text; break
        except AttributeError: cmp_name, cmp_link, cmp_image = "", "", "",  
    
    if cmp_name == "": return cmp_name, cmp_link, cmp_image

    cmp_link = cmp.get('href')
    
    driver.execute_script("window.open('about:blank', '_blank');")
    
    new_window_handle = driver.window_handles[-1]
    driver.switch_to.window(new_window_handle)

    driver.get(cmp_link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    

    cmp_image = get_cmp_image(soup)

    if randint(0, 10) % 2 == 0 :
        driver.execute_script(scroll_js)
    sleep(randint(2, 5))

    driver.close()
    driver.switch_to.window(driver.window_handles[1])

    return cmp_name, cmp_link.split("?")[0], cmp_image



    
# driver.get("https://www.indeed.com/cmp/Zelis-Healthcare?from=mobviewjob&tk=1hloqaq34ir1j800&fromjk=5a22c284e9d32468&attributionid=mobvjcmp")
# soup = BeautifulSoup(driver.page_source, 'html.parser')
def get_job(all_job_link: list, r: bool = False) -> None:
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
                if "This page isn’t working" in driver.page_source or "HTTP ERROR 429" in driver.page_source:
                    print("HTTP ERROR 429")
                    driver.refresh()
                    sleep(randint(2, 5))
                else:
                    break

            sleep(randint(5, 10))

            if "This job has expired on Indeed" in driver.page_source and 'Reasons could include: the employer is not accepting applications, is not actively hiring, or is reviewing applications' in driver.page_source:
                print(f"{i}) job has expired on Indeed, link: {job_link}")
                print("------------------------------------------------")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                # sleep(randint(3, 5))
                i += 1
                continue

            if randint(0, 10) % 2 == 0 :
                driver.execute_script(scroll_js)

            sleep(randint(1, 3))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # print( get_job_details(soup) )
            infos = get_job_details(driver)
            print( f"Job Link: {job_link}" )
            print( location(soup) )
            print( get_job_title(soup) )
            print( infos )
            cmp_name, cmp_link, cmp_image = get_cmp(soup, driver)
            print( f"cmp_name: {cmp_name.strip()}")
            print( f"cmp_link: {cmp_link.strip()}" )
            print( f"cmp_image: {cmp_image.strip()}" )
            print( f"remote: {r}" )
            # print( get_descriptions(soup) )

            source_obj, _ = Source.objects.get_or_create(source=SOURCE)
            # location_obj, _ = Location.objects.get_or_create(location=location(soup))
            location_obj, _ = Location.objects.get_or_create(location = country[scrape_index.loc_indeed_indx][0].lower() )

            job = Job.objects.create(
                title = get_job_title(soup),
                company = cmp_name.strip(),

                description = get_descriptions(soup), 
                
                job_link = job_link,
                company_url = cmp_link.strip(),
                image_url = cmp_image.strip(),

                specific_location = location(soup),
                remote = r,
                salary = infos["salary"],

                employment_type = infos['employment_type'],
            )

            job.source.add(source_obj)
            job.location.add(location_obj)
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
        else:
            get_job(list(job_link), True)
        

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


    if scrape_index.loc_indeed_indx < len(country_locations) - 1: scrape_index.loc_indeed_indx += 1
    else: scrape_index.loc_indeed_indx = 0
    scrape_index.save()

    print("Quit Driver")
    driver.quit()
    return "Done, Indeed."
