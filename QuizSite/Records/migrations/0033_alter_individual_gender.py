# Generated by Django 4.1.7 on 2023-06-25 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0032_individual_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='gender',
            field=models.BooleanField(blank=True, choices=[(True, 'Male'), (False, 'Female')], null=True),
        ),
    ]
