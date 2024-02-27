from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.http.response import JsonResponse

from pages.models import Job
from random import randint
from .serializers import JobSerializer


# Create your views here.
def api(request):
    jobs = Job.objects.all()
    json = {}
    inx = randint(0, len(jobs) - 1)

    job = jobs[inx]
    json['title'] = job.title
    json['company'] = job.company
    json['link'] = job.job_link

    json['salary'] = job.salary
    json['specific_location'] = job.specific_location
    json['lpublishink'] = job.publish
        
    return JsonResponse([json], safe=False)

class api_token(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]