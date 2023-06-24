from django.urls import path

from . import views

# from .views import LeagueListView

app_name = 'bracket'
urlpatterns = [
    path('', views.BracketListView.as_view(), name='bracket_list'),
    path('<int:pk>/', views.BracketEditView.as_view(), name='bracket'),
    path('create/', views.BracketCreateView.as_view(), name='bracket_create'),
    path('update/', views.update_match_score, name='update'),
    path('team/', views.TeamListView.as_view(), name='team_list'),
    path('team/<int:pk>/', views.TeamEditFormView.as_view(), name='team'),
    path('team/create/', views.TeamCreateFormView.as_view(), name='team_create'),
]
