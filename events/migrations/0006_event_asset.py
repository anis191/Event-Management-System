# Generated by Django 5.1.5 on 2025-02-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_rsvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, null=True, upload_to='events_asset'),
        ),
    ]
