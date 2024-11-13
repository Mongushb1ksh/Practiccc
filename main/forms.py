from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Application, Category
from django.contrib.auth.models import User
import re

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


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
        validators=[validate_full_name],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логин',
        max_length=30,
        validators=[validate_username],
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

    # Валидация, что пароли совпадают
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Пароли не совпадают.')

        # Проверка на уникальность логина
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят.')

        return cleaned_data