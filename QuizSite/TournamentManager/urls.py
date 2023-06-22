from django.urls import path

from . import views

# from .views import LeagueListView

app_name = 'manager'

urlpatterns = [
    # Used to pick material
    path('', views.index, name='index'),
    path('round_robin/', views.generate_matchups, name='round_robin'),
    path('event_generator/', views.populate_round_robbin_event, name='event_generator'),

]
