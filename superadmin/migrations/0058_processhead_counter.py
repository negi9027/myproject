# Generated by Django 4.2.7 on 2024-12-07 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0057_callingagent_counter_dispatchagent_counter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processhead',
            name='counter',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
