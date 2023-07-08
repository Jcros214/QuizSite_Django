# Generated by Django 4.1.7 on 2023-07-08 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='')),
                ('isTournament', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('birthday', models.DateField(blank=True, default=None, null=True, verbose_name='')),
                ('gender', models.BooleanField(blank=True, choices=[(True, 'Male'), (False, 'Female')], null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='')),
                ('material', models.CharField(max_length=100)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.league')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(blank=True, max_length=20, null=True)),
                ('division', models.CharField(blank=True, max_length=2, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.organization')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.season')),
            ],
            options={
                'unique_together': {('short_name', 'season'), ('name', 'organization', 'season')},
            },
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.individual')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.team')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.event')),
                ('quizmaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizmaster', to='Records.individual')),
                ('scorekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scorekeeper', to='Records.individual')),
            ],
            options={
                'unique_together': {('event', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('isValidated', models.BooleanField(default=False)),
                ('num_teams', models.IntegerField(default=3)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.event')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.room')),
            ],
        ),
        migrations.CreateModel(
            name='Progression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=10)),
                ('round', models.IntegerField()),
                ('division', models.CharField(max_length=30)),
                ('rank', models.IntegerField()),
                ('next_room', models.CharField(max_length=10)),
                ('next_round', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.event')),
                ('next_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_event', to='Records.event')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.league')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.organization')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.organization'),
        ),
        migrations.AddField(
            model_name='event',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.season'),
        ),
        migrations.CreateModel(
            name='AskedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('ruling', models.CharField(blank=True, max_length=100, null=True)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('bonusValue', models.IntegerField(blank=True, null=True)),
                ('bonusDescription', models.CharField(blank=True, max_length=100, null=True)),
                ('individual', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Records.individual')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizParticipants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isValidated', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.quiz')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.team')),
            ],
            options={
                'unique_together': {('quiz', 'team')},
            },
        ),
    ]
