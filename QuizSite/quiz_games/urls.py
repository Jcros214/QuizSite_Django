from django.urls import path

from . import views
# from .views import LeagueListView

app_name = 'quiz_games'

urlpatterns = [
    path('', views.index, name='index'),
]
