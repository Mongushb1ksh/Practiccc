from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    security_question  = models.ForeignKey('SecurityQuestion', on_delete=models.SET_NULL, null=True, blank=True)
    security_answer  = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.username

class SecurityQuestion(models.Model):
    question  = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.question

class UserSecurityAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    security_question  = models.ForeignKey(SecurityQuestion, on_delete=models.CASCADE)
    security_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Ответ безопасности для {self.user.username}"


# Модель для категорий заявок
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Модель заявки
class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'application/', blank=True, null=True)


    def __str__(self):
        return f'{self.title} ({self.status})'








