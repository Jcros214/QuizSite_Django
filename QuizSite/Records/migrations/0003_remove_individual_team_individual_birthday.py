# Generated by Django 4.1.7 on 2023-03-20 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0002_teammembership_quizparticipants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individual',
            name='team',
        ),
        migrations.AddField(
            model_name='individual',
            name='birthday',
            field=models.DateField(default=None, verbose_name=''),
        ),
    ]
