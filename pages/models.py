from django.db import models
from autoslug import AutoSlugField

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Source(models.Model):
    source = models.CharField(max_length=255)
    
    def __str__(self):
        return self.source

class Location(models.Model):
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.location

class Scrape(models.Model):
    loc_linkedin_indx = models.IntegerField()
    loc_indeed_indx = models.IntegerField()
    
    def __str__(self):
        return str(self.id)

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    
    description = models.TextField(null=True)

    job_link = models.URLField(max_length=300, null=True)
    company_url = models.URLField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)

    salary = models.CharField(max_length=255, null=True)

    source = models.ManyToManyField(Source)
    location = models.ManyToManyField(Location)
    specific_location = models.CharField(max_length=300, null=True)
    
    applications = models.CharField(max_length=255, null=True, blank=True)
    seniority_level = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(max_length=255, null=True, blank=True)
    Industries = models.CharField(max_length=255, null=True, blank=True)
    post_date = models.CharField(max_length=255, null=True, blank=True)
    remote = models.BooleanField(default=False, null=True)

    publish = models.DateTimeField(auto_now_add=True, null=True)
    slug = AutoSlugField(unique=True, populate_from='title', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}) {self.title}"

"""
Create New Token Every user created
"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)