# Generated by Django 4.2.7 on 2024-12-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0062_remove_callingagent_manager_processhead_enquiry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='process_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
