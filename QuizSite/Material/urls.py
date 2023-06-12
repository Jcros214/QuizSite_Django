from django.urls import path

from . import views

# from .views import LeagueListView

app_name = 'material'
urlpatterns = [
    # Used to pick material
    path('current-material/', views.current_material, name='current_material'),
    path('matthew/', views.matthew, name='matthew')
    # path('<int:material_id>', views.material, name="custom_material"),

    # Used to

    # # ex: /polls/
    # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
