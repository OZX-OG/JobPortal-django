# Generated by Django 4.2.9 on 2024-02-07 11:45

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='job',
            name='referral_link',
        ),
        migrations.AddField(
            model_name='job',
            name='Industries',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='company_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='employment_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='post_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='publish',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='seniority_level',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='title', unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='image_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ManyToManyField(to='pages.location'),
        ),
        migrations.AddField(
            model_name='job',
            name='source',
            field=models.ManyToManyField(to='pages.source'),
        ),
    ]