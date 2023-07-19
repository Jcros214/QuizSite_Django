from django.urls import path

from . import views

# from .views import LeagueListView

app_name = 'records'
urlpatterns = [
    path('', views.index, name='index'),
    path('league/<int:pk>/', views.LeagueDetailView.as_view(), name='league'),
    path('season/<int:pk>/', views.SeasonDetailView.as_view(), name='season'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event'),
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question'),
    path('individual/<int:pk>/', views.IndividualDetailView.as_view(), name='individual'),
    # path('event_summary/<int:event_id>/', views.event_summary, name='event_summary'),
    # path('live_display/event/<int:event_id>/', views.live_event_display, name='live_event_display'),
    # path('live_display/division/<int:division_id>/', views.live_division_display, name='live_division_display'),
    # path('live_display/division/<int:division_id>/table', views.live_division_display_table, name='live_division_display_table'),
    # path('live_display/divisions/<int:division_1_id>/<int:division_2_id>', views.live_divisions_display),
]
