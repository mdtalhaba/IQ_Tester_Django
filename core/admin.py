from django.contrib import admin
from .models import QuizScore

class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'score']

admin.site.register(QuizScore, QuizScoreAdmin)
