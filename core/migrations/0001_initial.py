# Generated by Django 4.2.6 on 2023-10-19 19:24

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePhysicalAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(blank=True, max_length=128, verbose_name='Address Line 1')),
                ('line_2', models.CharField(blank=True, max_length=128, verbose_name='Address Line 2')),
                ('line_3', models.CharField(blank=True, max_length=128, verbose_name='Address Line 3')),
                ('city', models.CharField(blank=True, max_length=64, verbose_name='City or Town')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('code', models.CharField(blank=True, max_length=12)),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.personnel')),
            ],
            options={
                'verbose_name': 'Physical Address',
                'verbose_name_plural': 'Physical Addresses',
            },
        ),
        migrations.CreateModel(
            name='AuthenticationAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Address')),
                ('person', models.ForeignKey(blank=True, limit_choices_to={'user__is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.personnel')),
            ],
            options={
                'verbose_name': 'Authentication Audit',
                'verbose_name_plural': 'Authentication Audits',
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddConstraint(
            model_name='authenticationaudit',
            constraint=models.UniqueConstraint(fields=('timestamp', 'ip_address'), name='authentication_audit_timestamp_ip_address'),
        ),
    ]