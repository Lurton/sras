# Generated by Django 4.2.6 on 2023-10-19 19:24

import core.utilities
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Campus')),
                ('location', models.CharField(max_length=64, verbose_name='Location')),
                ('address', models.CharField(max_length=128, verbose_name='Address')),
                ('path', models.CharField(max_length=32, unique=True)),
                ('email_address', models.EmailField(blank=True, help_text='This is the mailing group email address for the campus.', max_length=254, null=True, verbose_name='Email Address')),
                ('image', models.FileField(blank=True, null=True, upload_to=core.utilities.get_document_upload_path)),
            ],
            options={
                'verbose_name': 'Campus',
                'verbose_name_plural': 'Campuses',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Residence')),
                ('image', models.FileField(blank=True, null=True, upload_to=core.utilities.get_document_upload_path)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.campus')),
            ],
            options={
                'verbose_name': 'Residence',
                'verbose_name_plural': 'Residences',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=64, verbose_name='Residence')),
                ('floor', models.IntegerField(verbose_name='Floor')),
                ('image', models.FileField(blank=True, null=True, upload_to=core.utilities.get_document_upload_path)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='structure.residence')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Room',
                'ordering': ['number'],
            },
        ),
        migrations.AddConstraint(
            model_name='campus',
            constraint=models.UniqueConstraint(fields=('name',), name='campus_name'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('residence', 'number'), name='room_residence_number'),
        ),
        migrations.AddConstraint(
            model_name='residence',
            constraint=models.UniqueConstraint(fields=('name', 'campus'), name='residence_name_campus'),
        ),
    ]
