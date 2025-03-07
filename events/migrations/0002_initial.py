# Generated by Django 5.1.5 on 2025-03-07 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='assign_to',
            field=models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.category'),
        ),
        migrations.AddField(
            model_name='event',
            name='rsvp',
            field=models.ManyToManyField(blank=True, related_name='rsvp_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
