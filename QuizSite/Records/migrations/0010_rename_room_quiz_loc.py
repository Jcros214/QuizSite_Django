# Generated by Django 4.1.7 on 2023-03-20 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0009_alter_quiz_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='room',
            new_name='loc',
        ),
    ]
