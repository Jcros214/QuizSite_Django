from django.urls import path

from . import views
# from .views import LeagueListView

app_name = 'quiz_games'

urlpatterns = [
    path('', views.index, name='index'),
    path('match_verse/', views.match_verse, name='match_verse'),
    path('match_verse/backend/', views.match_verse_backend, name='match_verse_backend'),
]
