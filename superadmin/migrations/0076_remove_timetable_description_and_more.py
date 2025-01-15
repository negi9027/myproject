# Generated by Django 4.2.7 on 2025-01-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0075_hr_kra_timetable_callingagent_kras_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='description',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='ended_at',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='started_at',
        ),
        migrations.AddField(
            model_name='timetable',
            name='timetable',
            field=models.JSONField(default=[]),
        ),
    ]
