# Generated by Django 4.2.7 on 2024-12-28 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0069_notification_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='readby',
            new_name='unreadby',
        ),
    ]
