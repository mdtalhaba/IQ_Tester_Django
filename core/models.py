from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz

class Review(models.Model) :
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)