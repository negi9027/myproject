# Generated by Django 4.2.7 on 2024-12-28 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0073_alter_knowledgebank_hashtags_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knowledgebank',
            old_name='department',
            new_name='profile',
        ),
    ]
