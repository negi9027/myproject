# Generated by Django 5.1.1 on 2024-11-28 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0025_dispatchagent_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='superadmin',
            old_name='username',
            new_name='user_id',
        ),
    ]