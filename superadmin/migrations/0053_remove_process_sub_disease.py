# Generated by Django 4.2.7 on 2024-12-06 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0052_disease_callingagent_process_head_source_spend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='sub_disease',
        ),
    ]