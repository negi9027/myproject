# Generated by Django 4.2.7 on 2024-12-03 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0041_alter_enquiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='country',
            field=models.CharField(null=True),
        ),
    ]
