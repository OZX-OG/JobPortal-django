from rest_framework import serializers
from pages.models import Job

class JobSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Job
        # fields = '__all__'
        exclude = ['id', 'description']

    def get_source(self, obj):
        return [source.source for source in obj.source.all()][0]

    def get_location(self, obj):
        return [location.location for location in obj.location.all()]

