# Generated by Django 5.1.1 on 2024-11-29 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0038_remove_dme_sources_source_dmes_alter_enquiry_disease_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enquiry',
            old_name='interactions',
            new_name='dme_message',
        ),
    ]
