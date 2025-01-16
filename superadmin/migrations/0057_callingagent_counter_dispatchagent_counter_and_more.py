# Generated by Django 4.2.7 on 2024-12-07 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0056_dme_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='callingagent',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='dispatchagent',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='process',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='teamleader',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]