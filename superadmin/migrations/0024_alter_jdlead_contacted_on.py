# Generated by Django 5.1.1 on 2024-11-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0023_alter_jdlead_area_alter_jdlead_brancharea_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jdlead',
            name='contacted_on',
            field=models.CharField(blank=True, null=True),
        ),
    ]
