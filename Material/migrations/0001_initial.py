# Generated by Django 4.1.7 on 2023-07-08 21:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Genesis', 'Genesis'), ('Exodus', 'Exodus'), ('Leviticus', 'Leviticus'), ('Numbers', 'Numbers'), ('Deuteronomy', 'Deuteronomy'), ('Joshua', 'Joshua'), ('Judges', 'Judges'), ('Ruth', 'Ruth'), ('1 Samuel', '1 Samuel'), ('2 Samuel', '2 Samuel'), ('1 Kings', '1 Kings'), ('2 Kings', '2 Kings'), ('1 Chronicles', '1 Chronicles'), ('2 Chronicles', '2 Chronicles'), ('Ezra', 'Ezra'), ('Nehemiah', 'Nehemiah'), ('Esther', 'Esther'), ('Job', 'Job'), ('Psalms', 'Psalms'), ('Proverbs', 'Proverbs'), ('Ecclesiastes', 'Ecclesiastes'), ('Song of Solomon', 'Song of Solomon'), ('Isaiah', 'Isaiah'), ('Jeremiah', 'Jeremiah'), ('Lamentations', 'Lamentations'), ('Ezekiel', 'Ezekiel'), ('Daniel', 'Daniel'), ('Hosea', 'Hosea'), ('Joel', 'Joel'), ('Amos', 'Amos'), ('Obadiah', 'Obadiah'), ('Jonah', 'Jonah'), ('Micah', 'Micah'), ('Nahum', 'Nahum'), ('Habakkuk', 'Habakkuk'), ('Zephaniah', 'Zephaniah'), ('Haggai', 'Haggai'), ('Zechariah', 'Zechariah'), ('Malachi', 'Malachi'), ('Matthew', 'Matthew'), ('Mark', 'Mark'), ('Luke', 'Luke'), ('John', 'John'), ('Acts', 'Acts'), ('Romans', 'Romans'), ('1 Corinthians', '1 Corinthians'), ('2 Corinthians', '2 Corinthians'), ('Galatians', 'Galatians'), ('Ephesians', 'Ephesians'), ('Philippians', 'Philippians'), ('Colossians', 'Colossians'), ('1 Thessalonians', '1 Thessalonians'), ('2 Thessalonians', '2 Thessalonians'), ('1 Timothy', '1 Timothy'), ('2 Timothy', '2 Timothy'), ('Titus', 'Titus'), ('Philemon', 'Philemon'), ('Hebrews', 'Hebrews'), ('James', 'James'), ('1 Peter', '1 Peter'), ('2 Peter', '2 Peter'), ('1 John', '1 John'), ('2 John', '2 John'), ('3 John', '3 John'), ('Jude', 'Jude'), ('Revelation', 'Revelation')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(150)])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.book')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('symbol', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(176)])),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.questiontype')),
                ('verse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.verse')),
            ],
        ),
    ]
