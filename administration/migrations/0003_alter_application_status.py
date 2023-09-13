# Generated by Django 4.2.4 on 2023-09-13 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Submitted'), (2, 'In Review'), (3, 'Approved'), (4, 'Rejected'), (5, 'Terminated')], default=1, verbose_name='Application Status'),
        ),
    ]