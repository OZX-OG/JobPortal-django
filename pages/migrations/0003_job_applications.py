# Generated by Django 4.2.9 on 2024-02-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_location_source_remove_job_referral_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applications',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
