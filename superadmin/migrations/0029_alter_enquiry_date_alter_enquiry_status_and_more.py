# Generated by Django 5.1.1 on 2024-11-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0028_alter_enquiry_address_alter_enquiry_agent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='status',
            field=models.CharField(default='chat', max_length=50),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
