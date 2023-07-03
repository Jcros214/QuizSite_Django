from django.contrib import admin

# Register your models here.
from .models import QuestionType, Question

admin.site.register(QuestionType)
admin.site.register(Question)
