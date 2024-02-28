from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Job, Source, Location
from .task import scrape_indeed, scrape_linkedin, clear_jobs_fromDB

# Create your views here.
def index(request): 
    print(f"request.method: {request.method}")
    print(f"GET: {request.GET}")
    print(f"Post: {request.POST}")


    jobs = Job.objects.all()
    locations = Location.objects.all()

    checkbox_filters = {
        'full_time': 'Full-time',
        'part_time': 'Part-time',
        'contract': 'Contract',
        'remote': True,
        'internship': 'Internship',

    }

    source = {
        'linkedin': 'Linkedin',
        'indeed': 'Indeed',
    }

    filter_conditions = []

    # Iterate through each checkbox and add its filter condition if checked
    for checkbox, filter_value in checkbox_filters.items():
        if request.GET.get(checkbox):
            if isinstance(filter_value, bool):  # For boolean fields
                filter_conditions.append(Q(remote=filter_value))
            else:
                print(filter_value)
                filter_conditions.append(Q(employment_type=filter_value))
                
    # Filter by location if it's provided in the request
    
    location_param = request.GET.get('location')
    if location_param:
        if not location_param == 'anywhere':
            filter_conditions.append(Q(location__location__icontains=location_param))
    
    for checkbox, filter_value in source.items():
        if request.GET.get(checkbox):
            source_obj = Source.objects.get(source=filter_value)
            print(f"source_obj: {source_obj}")
            filter_conditions.append(Q(source=source_obj))
    
    print(f"locations: {list(locations)}")
    print(f"filter_conditions: {filter_conditions}")
    print(f'Sort: {request.GET.get("sort")}')

    # Apply all filter conditions using bitwise OR operation
    if filter_conditions:
        jobs = jobs.filter(*filter_conditions)
        
    print(len(jobs))
    jobs = list(jobs)
    jobs.reverse()

    page = Paginator(jobs, 10).get_page( request.GET.get("page") )
    
    if request.GET.get("sort") == 'otn':
        jobs.reverse()
        page = Paginator(jobs, 10).get_page( request.GET.get("page") )



    context = {
        'jobs_count': len(jobs),
        "page": page,
        "locations": locations,
        }

    return render(request, 'pages/index.html', context)

def job_details(request, slug): 

    # scrape_and_update_jobs.delay()
    # return HttpResponse("lets go")
    job = Job.objects.get(slug=slug)
 
    context = {'job': job}


    return render(request, 'pages/job_details.html', context)


def scrape_linkedin_jobs(request): 
    scrape_linkedin.delay()
    return HttpResponse("start scraping jobs fron Linkedin")

def scrape_indeed_jobs(request): 
    scrape_indeed.delay()
    return HttpResponse("start scraping jobs fron Indeed")

def clear_scrape(request): 
    clear_jobs_fromDB.delay()
    return HttpResponse("Clear all The unavailable jobs, from Linkedin and Indeed")


# def job_details(request):



