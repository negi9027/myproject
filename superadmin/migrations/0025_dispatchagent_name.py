# Generated by Django 5.1.1 on 2024-11-28 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0024_alter_jdlead_contacted_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchagent',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
