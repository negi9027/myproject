# Generated by Django 4.2.7 on 2024-12-16 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0063_enquiry_process_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='disease_code',
        ),
    ]