# Generated by Django 5.1.1 on 2024-11-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallingAgent',
            fields=[
                ('agent_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('is_enabled', models.BooleanField(default=True)),
                ('login_times', models.JSONField()),
                ('permissions', models.JSONField()),
                ('department', models.CharField(default='Calling', max_length=50)),
                ('team_leader', models.JSONField()),
                ('manager', models.JSONField()),
                ('targets', models.JSONField()),
                ('interactions', models.JSONField()),
                ('conversion_rate', models.JSONField()),
                ('failed_deals', models.JSONField()),
                ('attendance', models.JSONField()),
            ],
            options={
                'db_table': 'callingagent',
            },
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('delivery_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('agent_id', models.CharField(max_length=20)),
                ('delivery_company', models.CharField(max_length=100)),
                ('deliveries', models.JSONField()),
                ('products', models.JSONField()),
                ('calling_agent_id', models.CharField(max_length=20)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('area', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('received_by', models.CharField(max_length=100)),
                ('patient_id', models.CharField(max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('delivery_status', models.CharField(choices=[('Delivered', 'Delivered'), ('Returned', 'Returned'), ('Lost', 'Lost')], max_length=20)),
                ('advance_cod', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('UPI', 'UPI'), ('Card', 'Card')], max_length=20)),
                ('payment_source', models.CharField(max_length=50)),
                ('conversion_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_to_deliver', models.DurationField()),
                ('patient_review', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dispatch',
            },
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('enquiry_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('source', models.CharField(max_length=500)),
                ('patient_id', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('disease', models.CharField(max_length=255)),
                ('organ', models.CharField(max_length=255)),
                ('interactions', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('time', models.TimeField()),
                ('landing_page', models.URLField(blank=True, max_length=255, null=True)),
                ('utm_source', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_campaign', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_ad', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_browser', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_device', models.CharField(blank=True, max_length=255, null=True)),
                ('utm_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('utm_others', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=50)),
                ('conversion_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('products', models.JSONField(blank=True, null=True)),
                ('failed_deals', models.JSONField(blank=True, null=True)),
                ('demographics', models.JSONField(blank=True, null=True)),
                ('app', models.JSONField(blank=True, null=True)),
                ('duplicate', models.BooleanField(default=False)),
                ('retention', models.JSONField(blank=True, null=True)),
                ('visit_history', models.JSONField(blank=True, null=True)),
                ('agent', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'enquiry',
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hospital_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('receptionist_id', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('doctor', models.JSONField()),
                ('enquiry', models.JSONField()),
                ('patients', models.JSONField()),
                ('medicines', models.JSONField()),
                ('employees', models.JSONField()),
                ('expected_patients', models.JSONField()),
                ('revenue', models.JSONField()),
                ('ward_numbers', models.JSONField()),
                ('beds', models.JSONField()),
            ],
            options={
                'db_table': 'hospitals',
            },
        ),
        migrations.CreateModel(
            name='jdlead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leadid', models.CharField(max_length=255, unique=True)),
                ('leadtype', models.CharField(max_length=255)),
                ('prefix', models.CharField(blank=True, max_length=10, null=True)),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=15)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('brancharea', models.CharField(max_length=255)),
                ('dncmobile', models.IntegerField()),
                ('dncphone', models.IntegerField()),
                ('company', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=10)),
                ('time', models.TimeField()),
                ('branchpin', models.CharField(max_length=6)),
                ('parentid', models.CharField(max_length=255)),
                ('contacted', models.BooleanField(default=False)),
                ('interested', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'jdlead',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('medicine_code', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('diseases', models.JSONField()),
                ('organs', models.JSONField()),
                ('strength', models.CharField(choices=[('Major', 'Major'), ('Minor', 'Minor')], max_length=10)),
                ('countries_available', models.JSONField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('margin', models.DecimalField(decimal_places=2, max_digits=5)),
                ('out_of_stock', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'medicine',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('source_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('country', models.CharField(choices=[('India', 'India'), ('USA', 'USA'), ('UK', 'UK'), ('Other', 'Other')], max_length=100)),
                ('disease', models.CharField(choices=[('Kidney', 'Kidney'), ('Cancer', 'Cancer'), ('Parkinsons', 'Parkinsons'), ('Liver', 'Liver'), ('Other', 'Other')], max_length=100)),
                ('platform', models.CharField(choices=[('website', 'Website'), ('youtube', 'YouTube'), ('instagram', 'Instagram'), ('google', 'Google'), ('facebook', 'Facebook'), ('call', 'Call')], max_length=100)),
                ('platform_link', models.CharField(max_length=200)),
                ('medium', models.CharField(choices=[('chat', 'Chat'), ('phone', 'Phone'), ('webform', 'Webform')], max_length=100)),
                ('enquiry_type', models.CharField(choices=[('Organic', 'Organic'), ('Inorganic', 'Inorganic')], max_length=10)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'source',
            },
        ),
        migrations.CreateModel(
            name='Superadmin',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'superadmin',
            },
        ),
    ]
