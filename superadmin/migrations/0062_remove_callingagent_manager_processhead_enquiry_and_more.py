# Generated by Django 4.2.7 on 2024-12-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0061_remove_enquiry_disease_enquiry_sub_disease'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callingagent',
            name='manager',
        ),
        migrations.AddField(
            model_name='processhead',
            name='enquiry',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='teamleader',
            name='enquiry',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='processhead',
            name='department',
            field=models.CharField(default='Calling', editable=False),
        ),
        migrations.AlterField(
            model_name='processhead',
            name='profile',
            field=models.CharField(default='processhead', editable=False),
        ),
    ]
