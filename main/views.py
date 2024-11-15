from importlib.metadata import requires
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm, ApplicationStatusForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Application, Category, CustomUser, SecurityQuestion, UserSecurityAnswer
from .forms import ApplicationForm, CategoryForm, ApplicationStatusForm, PasswordResetBySecurityForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings







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
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']


            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                security_question=question,
                security_answer=answer,
            )
            user.first_name = full_name
            user.save()

            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, введите коректные данные')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def password_reset_by_security(request):
    if request.method == 'POST':
        form = PasswordResetBySecurityForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']

            try:
                user = CustomUser.objects.get(username=username)

                if user.security_question.id == question and user.security_answer == answer:
                    return render(request, 'registration/password_reset_success.html', {'user': user})
                else:
                    messages.error(request, 'Неверный ответ на вопрос безопасности.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Пользователь с таким именем не найден.')
            except UserSecurityAnswer.DoesNotExist:
                messages.error(request, 'Нет информации о вопросе безопасности для этого пользователя.')

            return render(request, 'registration/password_reset_success.html', {'user': user})

    else:
        form = PasswordResetBySecurityForm()

    return render(request, 'registration/password_reset_by_security.html', {'form': form})

def password_reset_success(request, user_id):
    user = User.objects.get(id=user_id)
    password = user.password
    return render(request, 'password_reset_success.html', {'password': password})


class ApplicationListView( ListView):
    model = Application
    template_name = 'main/index.html'
    context_object_name  = 'applications'

    def get_queryset(self):
        return Application.objects.all().order_by('-created_at')[:4]


class MyApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'main/user_application_list.html'
    context_object_name = 'applications'

    def test_func(self):
        application = self.get_object()
        return application.user == self.request.user


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.user = request.user
                application.save()

                messages.success(request, 'Вы успешно создали форму')
                return redirect("application")
            except Exception as e:
                print(f"Ошибка при сохранении изображения: {e}")
    else:
        form = ApplicationForm()
    return render(request, 'main/application_form.html', {'form': form})


class ApplicationDetailView(DetailView):
    model = Application
    template_name = 'main/application_detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['status_form'] = ApplicationStatusForm(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        application = self.get_object()

        if request.user.is_superuser:
            form = ApplicationStatusForm(request.POST, instance=application)

            if form.is_valid():
                form.save()
                return redirect('application_detail', pk=application.pk)

        return redirect('error')





class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'main/applcation_delete.html'
    success_url = reverse_lazy('application')

    def test_func(self):
        application = self.get_object()
        return application.user == self.request.user

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_create.html'
    success_url = reverse_lazy('category_list')

    def get_permission_required(self):
        return ['main.add_category']

def category_list(request):
    categories = Category.objects.all()  # Получаем все категории из базы данных
    return render(request, 'main/category_list.html', {'categories': categories})

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return render(request, 'main/category_list.html')

    return render(request, 'main/category_delete.html', {'category': category})

def profile_view(request):
    return render(request, 'main/profile.html')




