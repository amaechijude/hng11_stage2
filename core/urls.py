
from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('auth/register', views.register, name='register'),
        path('auth/login', views.login_user, name='login_user'),
        path('api/users/<str:id>', views.user_detail, name='user_detail'),
        path('api/organisations', views.org_view.as_view(), name='org_view'),
        path('api/organisations/<str:orgId>', views.Org_details.as_view(), name='org_details'),
        path('api/create/organisations', views.create_org, name='create_org'),
        path('api/organisations/<str:orgId>/users', views.add_users, name='add_users'),

        ]
