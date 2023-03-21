# Generated by Django 4.1.7 on 2023-03-20 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0011_remove_quiz_event_remove_quiz_quizmaster_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.event')),
                ('quizmaster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.individual')),
            ],
        ),
        migrations.CreateModel(
            name='QuizParticipants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.quiz')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.individual')),
            ],
        ),
        migrations.CreateModel(
            name='AskedQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruleing', models.CharField(max_length=100)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.individual')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Records.quiz')),
            ],
        ),
    ]
