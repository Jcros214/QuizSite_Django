from django import template
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

try:
    from Records.models import *
except ImportError:
    from ...Records.models import *

register = template.Library()

# def render_team(team: Team, event: Event) -> str:
#     current_quiz = event.get_team_current_quiz(team)
#     next_quiz = event.get_team_next_quiz(team)
#
#     values = {
#         'rank': event.get_team_rank(team),
#         'code': team.short_name,
#         'team_name': team.name,
#         'score': event.get_team_score(team),
#         'current': f"<a href='{current_quiz.get_absolute_url()}'>{current_quiz}</a>",
#         'next': f"<a href='{next_quiz.get_absolute_url()}'>{next_quiz}</a>",
#         'quizzers': '<br>'.join([str(team) for team in team.get_individuals()]),
#         # 'quizzer_scores': '<br>'.join(
#         #     [str(event.get_individual_score(individual)) for individual in team.get_individuals()]),
#     }
#
#     return f"<tr>{''.join([f'<td>{value}</td>' for value in values.values()])}</tr>"
#


# def render_team_row(team: dict) -> str:
#     def render_quiz(quiz: Quiz) -> str:
#         return f"<a href='{quiz.get_absolute_url()}'>{quiz.room} - {quiz.round}</a>"
#
#     current_round_object = Quiz.objects.filter(pk=team['current_round'])
#     if current_round_object.exists():
#         team['current_quiz_string'] = render_quiz(current_round_object.first())
#
#     next_round_object = Quiz.objects.filter(pk=team['next_round'])
#     if next_round_object.exists():
#         team['next_quiz_string'] = render_quiz(next_round_object.first())
#
#     html = f"""
#          <tr>
#              <td>{team['rank']}</td>
#              <td>{team['code']}</td>
#              <td>{team['name'].replace(' ', '&nbsp;')}</td>
#              <td>{team['score']}</td>
#             <td>{team.get('current_quiz_string', ' -- ')}</td>
#             <td>{team.get('next_quiz_string', ' -- ')}</td>
#              <td>
#                  {' / '.join([str(quizzer['name']) for quizzer in team['individuals']]).replace(' ', '&nbsp;')}
#              </td>
#          </tr>
#          """
#     return html


division_colors = {
    'R': 'danger',
    'B': 'primary',
}


def render_division_table(name: str, teams: List[Team]) -> str:
    color = division_colors.get(name, '')

    html = f'''
<table class="table table-sm table-{color}">
    <thead>
        <tr>
            <th>Rank</th>
            <th>Code</th>
            <th>Team Name</th>
            <th>Score</th>
            <th>Quizzers</th>
        </tr>                
    </thead>
'''

    for team in division_data:
        #         if team['rank'] > 6 and caches.get('champ') is None:
        #             caches['champ'] = prv_score
        #         elif team['rank'] > 12 and caches.get('champ') is None:
        #             caches['cons1'] = prv_score
        #
        html += render_team_row(team)
    html += '\n</table>'
    return html


def render_a_division_table(division: Division) -> str:
    data = division.get_division_view_data()

    return format_html(render_division_table(data, division))


####################################################################################################
#                                                                                                  #
#                                                                                                  #
#                                        Used tags/filters                                         #
#                                                                                                  #
#                                                                                                  #
####################################################################################################


"""

<div class="division-table division-red col-5" hx-get="{reverse('records:live_division_display_table', kwargs={'division_id': division.id})}" hx-trigger="every 2s">

"""


@register.simple_tag()
def ranked_teams_table(event: Event):
    html = '''
    <table class="table">
        <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Score</th>
            <th>Type</th>
            <th>Individuals</th>
        </tr>
    '''
    for team in event.get_ranked_teams():
        html += f'''
        <tr>
            <td>{team.rank}</td>
            <td><a href="{team.get_absolute_url()}">{team.name}</a></td>
            <td>{team.score}</td>
            <td>{team.type.capitalize() if team.type else ' - '}</td>
            <td>{' / '.join([f'<a href="{team.get_absolute_url()}">{team.name}</a>' for team in team.get_individuals()])}</td>
        </tr>
        '''
    html += '</table>'

    return format_html(html)


@register.simple_tag()
def ranked_individuals_table(event: Event):
    html = '''
    <table class="table">
        <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Team</th>
            <th>Score</th>
        </tr>
    '''
    for individual in event.get_ranked_individuals():
        team = Team.objects.get(pk=individual.events_team)
        html += f'''
        <tr>
            <td>{individual.rank}</td>
            <td><a href="{individual.get_absolute_url()}">{individual.name}</a></td>
            <td><a href="{team.get_absolute_url()}">{team.name}</a></td>
            <td>{individual.score}</td>
        </tr>
        '''
    html += '</table>'

    return format_html(html)
