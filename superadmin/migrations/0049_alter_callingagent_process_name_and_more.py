# Generated by Django 4.2.7 on 2024-12-05 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0048_alter_callingagent_process_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callingagent',
            name='process_name',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='teamleader',
            name='process_name',
            field=models.JSONField(null=True),
        ),
    ]
