from django.contrib import admin
from .models import Job, Source, Location, Scrape

# Register your models here.
class JobAdmin(admin.ModelAdmin):

    def display_source(self, obj):
        return ", ".join([source.source for source in obj.source.all()])
    display_source.short_description = 'source'

    def display_locations(self, obj):
        return ", ".join([location.location for location in obj.location.all()])
    display_locations.short_description = 'location'
    

    list_display = ['title', 'display_source', 'company',  'display_locations' ,'salary', 'applications', 'seniority_level', 'employment_type', 'remote', 'post_date', 'publish']


admin.site.register(Job, JobAdmin)
admin.site.register(Source)
admin.site.register(Location)
admin.site.register(Scrape)