# Generated by Django 3.2.19 on 2023-06-02 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bracket', '0017_match_is_upper_child'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='division',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1_seed',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2_seed',
        ),
        migrations.AlterField(
            model_name='match',
            name='parent_match',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_match', to='Bracket.match'),
        ),
    ]
