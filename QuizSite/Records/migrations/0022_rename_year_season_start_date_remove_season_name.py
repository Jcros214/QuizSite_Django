# Generated by Django 4.1.7 on 2023-06-16 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0021_alter_individual_birthday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='season',
            old_name='year',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='season',
            name='name',
        ),
    ]
