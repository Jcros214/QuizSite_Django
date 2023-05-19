from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('regsignupister/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
