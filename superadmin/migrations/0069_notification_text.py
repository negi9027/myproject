# Generated by Django 4.2.7 on 2024-12-28 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0068_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
