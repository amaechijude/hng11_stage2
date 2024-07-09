
from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('auth/register', views.register, name='register'),

        ]
