# Generated by Django 4.2 on 2023-07-15 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0004_quizprogression_allow_ties_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quizparticipants',
            unique_together=set(),
        ),
    ]
