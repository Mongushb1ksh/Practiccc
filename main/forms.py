from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Application, Category, SecurityQuestion, UserSecurityAnswer, CustomUser
from django.contrib.auth.models import User
from django.conf import settings
import re

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Application.STATUS_CHOICES),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']





def validate_full_name(value):
    if not re.match(r'^[А-Яа-яЁё\s\-]+$', value):
        raise ValidationError('ФИО должно содержать только кириллические буквы, дефисы и пробелы.')

def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9\-]+$', value):
        raise ValidationError('Логин должен содержать только латиницу и дефис.')


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        validators=[validate_full_name],  # Предположим, что это ваша кастомная валидация
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логин',
        max_length=30,
        validators=[validate_username],  # Предположим, что это ваша кастомная валидация
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # Контрольный вопрос и ответ
    question = forms.ModelChoiceField(
        queryset=SecurityQuestion.objects.all(),
        required=True,
        label="Выберите контрольный вопрос"
    )
    answer = forms.CharField(
        required=True,
        label="Ответ на вопрос безопасности",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Валидация данных
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Проверка совпадения паролей
        if password != confirm_password:
            raise ValidationError('Пароли не совпадают.')

        # Проверка на уникальность логина
        username = cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят.')

        # Проверка на наличие вопроса и ответа
        question = cleaned_data.get('question')
        answer = cleaned_data.get('answer')
        if not question or not answer:
            raise ValidationError('Контрольный вопрос и ответ не могут быть пустыми.')

        return cleaned_data

    def save(self, commit=True):
        # Создаем пользователя
        user = CustomUser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            full_name=self.cleaned_data['full_name']  # Добавляем поле для ФИО
        )
        user.set_password(self.cleaned_data['password'])  # Обязательно хэшируем пароль
        if commit:
            user.save()

        # Создаем запись в UserSecurityAnswer
        question = self.cleaned_data['question']
        answer = self.cleaned_data['answer']
        UserSecurityAnswer.objects.create(
            user=user,
            question=question,
            answer=answer
        )

        return user

class PasswordResetBySecurityForm(forms.Form):
    username = forms.CharField(max_length=150)
    question = forms.ModelChoiceField(queryset=SecurityQuestion.objects.all())
    answer = forms.CharField(max_length=255)