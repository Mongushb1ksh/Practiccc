from django.contrib import admin
from .models import Category, Application
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SecurityQuestion, UserSecurityAnswer

class CustomUserAdmin(UserAdmin):
    # Стандартные поля для отображения
    list_display = ('username', 'email', 'first_name', 'last_name', 'security_question', 'security_answer')

    # Определяем методы для получения вопросов и ответов
    def get_security_question(self, obj):
        try:
            answer = UserSecurityAnswer.objects.get(user=obj)
            return answer.question.question  # Извлекаем вопрос из связи с UserSecurityAnswer
        except UserSecurityAnswer.DoesNotExist:
            return 'No question set'
    get_security_question.short_description = 'Security Question'

    def get_security_answer(self, obj):
        try:
            answer = UserSecurityAnswer.objects.get(user=obj)
            return answer.answer  # Извлекаем ответ на контрольный вопрос
        except UserSecurityAnswer.DoesNotExist:
            return 'No answer set'
    get_security_answer.short_description = 'Security Answer'

# Регистрируем кастомную модель пользователя
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SecurityQuestion)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(UserSecurityAnswer)
# Register your models here.
