# Generated by Django 5.1.1 on 2024-11-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0008_alter_processhead_table_alter_teamleader_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='beds',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='doctor',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='employees',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='enquiry',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='expected_patients',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='medicines',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='patients',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='revenue',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='ward_numbers',
            field=models.JSONField(blank=True, null=True),
        ),
    ]