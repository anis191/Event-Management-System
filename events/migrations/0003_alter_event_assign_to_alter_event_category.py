# Generated by Django 5.1.5 on 2025-02-02 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_assign_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='assign_to',
            field=models.ManyToManyField(related_name='events', to='events.participant'),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.category'),
        ),
    ]
