# Generated by Django 4.2.5 on 2023-10-14 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_transfer_termination_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='application',
            name='application_student',
        ),
    ]