# Generated by Django 3.2.19 on 2023-06-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bracket', '0016_match_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='is_upper_child',
            field=models.BooleanField(default=False),
        ),
    ]
