from django.urls import path

from . import views

# from .views import LeagueListView

app_name = 'records'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:league_id>/', views.league, name='league'),
    path('<int:league_id>/<int:season_id>/', views.season, name='season'),
    path('<int:league_id>/<int:season_id>/<int:event_id>/', views.event, name='event'),
    path('<int:league_id>/<int:season_id>/team/<int:team_id>', views.team, name='team'),
    path('<int:league_id>/<int:season_id>/<int:event_id>/<int:quiz_id>/', views.quiz, name='quiz'),
    path('<int:league_id>/<int:season_id>/<int:event_id>/<int:quiz_id>/<int:question_id>/', views.question,
         name='question'),
    path('user/<int:individual_id>/', views.individual, name='individual'),
    path('event_summary/<int:event_id>/', views.event_summary, name='event_summary'),

    # # ex: /polls/
    # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
