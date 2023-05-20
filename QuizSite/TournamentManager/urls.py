from django.urls import path

from . import views
# from .views import LeagueListView

app_name = 'manager'

urlpatterns = [
    # Used to pick material
    path('', views.index, name='index'),
    path('round_robbin/', views.round_robbin, name='round_robbin'),
]
