from importlib.metadata import requires

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Application, Category
from .forms import ApplicationForm, CategoryForm
from django.contrib.auth.mixins import PermissionRequiredMixin




def is_admin(user):
    return user.is_staff


def home(request):
    return render(request, 'basic.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():# Если форма прошла валидацию, создаем нового пользователя
            username = form.cleaned_data['username']
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = full_name
            user.save()

            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')  # Успешная регистрация
        else:
            messages.error(request, 'Пожалуйста, введите коректные данные')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'main/index.html'
    context_object_name  = 'applications'

@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)  # Не сохраняем сразу
            application.user = request.user  # Назначаем пользователя
            application.save()  # Сохраняем объект с пользователем

            messages.success(request, 'Вы успешно создали форму')
            return redirect("application")
    else:
        form = ApplicationForm()
    return render(request, 'main/application_form.html', {'form': form})

# class ApplicationCreateView(LoginRequiredMixin, CreateView):
#     model = Application
#     form_class = ApplicationForm
#     template_name = 'main/application_form.html'
#     success_url = reverse_lazy('application')
#     image = .FILES.get('image')
#
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)




class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'main/application_detail.html'
    context_object_name = 'application'


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'main/applcation_delete.html'
    success_url = reverse_lazy('application')

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_create.html'

    def get_permission_required(self):
        # Возвращаем разрешение, которое требуется для создания категории
        return ['main.add_category']

class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('application')
    permission_required = 'main.delete_category'




