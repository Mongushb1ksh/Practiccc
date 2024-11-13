from django.urls import path
from . import views
from .views import ApplicationDeleteView

urlpatterns = [
    path('', views.home, name='basic'),
    path('index/', views.ApplicationListView.as_view(), name='application'),
    path('register/', views.register, name='register'),
    # path('application/', views.ApplicationListView.as_view(), name='application'),
    path('application/create/', views.application_create, name='application_create'),
    path('application/<int:pk>', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('application/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='applcation_delete'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

]
