from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz

class Review(models.Model) :
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)


class QuizScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="quiz_score")
    score = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    quiz_count = models.IntegerField(blank=True, null=True, default=0)