# Generated by Django 4.2.7 on 2024-12-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0053_remove_process_sub_disease'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='type',
            field=models.CharField(choices=[('Aquisition', 'Aquisition'), ('Retention', 'Retention')], default='Aquisition', max_length=100),
        ),
    ]
