from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.username


class Question(models.Model):
    question_text = models.CharField(max_length=255) 
    option_1 = models.CharField(max_length=255)  
    option_2 = models.CharField(max_length=255)  
    option_3 = models.CharField(max_length=255)  
    option_4 = models.CharField(max_length=255)  
    correct_answer = models.CharField(max_length=255)  

    def __str__(self):
        return self.question_text
