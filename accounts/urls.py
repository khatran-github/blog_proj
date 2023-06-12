from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]