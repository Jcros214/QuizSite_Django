from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class QuestionType(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Question(models.Model):
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)

    book = models.CharField(choices=(
        (1, 'Genesis'), (2, 'Exodus'), (3, 'Leviticus'), (4, 'Numbers'), (5, 'Deuteronomy'), (6, 'Joshua'),
        (7, 'Judges'),
        (8, 'Ruth'), (9, '1 Samuel'), (10, '2 Samuel'), (11, '1 Kings'), (12, '2 Kings'), (13, '1 Chronicles'),
        (14, '2 Chronicles'), (15, 'Ezra'), (16, 'Nehemiah'), (17, 'Esther'), (18, 'Job'), (19, 'Psalms'),
        (20, 'Proverbs'),
        (21, 'Ecclesiastes'), (22, 'Song of Solomon'), (23, 'Isaiah'), (24, 'Jeremiah'), (25, 'Lamentations'),
        (26, 'Ezekiel'), (27, 'Daniel'), (28, 'Hosea'), (29, 'Joel'), (30, 'Amos'), (31, 'Obadiah'), (32, 'Jonah'),
        (33, 'Micah'), (34, 'Nahum'), (35, 'Habakkuk'), (36, 'Zephaniah'), (37, 'Haggai'), (38, 'Zechariah'),
        (39, 'Malachi'), (40, 'Matthew'), (41, 'Mark'), (42, 'Luke'), (43, 'John'), (44, 'Acts'), (45, 'Romans'),
        (46, '1 Corinthians'), (47, '2 Corinthians'), (48, 'Galatians'), (49, 'Ephesians'), (50, 'Philippians'),
        (51, 'Colossians'), (52, '1 Thessalonians'), (53, '2 Thessalonians'), (54, '1 Timothy'), (55, '2 Timothy'),
        (56, 'Titus'), (57, 'Philemon'), (58, 'Hebrews'), (59, 'James'), (60, '1 Peter'), (61, '2 Peter'),
        (62, '1 John'),
        (63, '2 John'), (64, '3 John'), (65, 'Jude'), (66, 'Revelation')), max_length=20)

    chapter = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(150)])
    verse = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(176)])

    prompt = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f"<Question {self.book} {self.chapter}:{self.verse}>"
