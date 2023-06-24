# Generated by Django 4.1.7 on 2023-06-23 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0030_team_short_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.event')),
            ],
        ),
    ]
