# Generated by Django 4.1.7 on 2023-03-20 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Records', '0008_alter_quiz_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='room',
            field=models.CharField(default='A', max_length=10),
            preserve_default=False,
        ),
    ]
