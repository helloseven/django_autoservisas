from django.urls import path

from . import views

app_name = 'user_profile'
urlpatterns = [
     path('register/', views.UserRegisterView.as_view(), name='register'),
     path('profile/', views.profile, name='profile'),
]
