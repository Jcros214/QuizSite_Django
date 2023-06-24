# Generated by Django 3.2.19 on 2023-05-24 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bracket', '0006_bracket_num_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bracket',
            name='num_teams',
            field=models.IntegerField(default=16),
        ),
        migrations.DeleteModel(
            name='AllowedNumberOfTeams',
        ),
    ]
