# Generated by Django 5.1.1 on 2024-11-22 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0011_alter_teamleader_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callingagent',
            name='user_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
