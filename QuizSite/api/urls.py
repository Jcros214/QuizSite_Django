from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('records/', views.register, name='register'),
]