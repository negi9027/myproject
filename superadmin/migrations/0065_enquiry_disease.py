# Generated by Django 4.2.7 on 2024-12-16 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0064_remove_enquiry_disease_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='disease',
            field=models.CharField(max_length=30, null=True),
        ),
    ]