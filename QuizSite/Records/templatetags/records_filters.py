from django import template
from django.utils.html import format_html

try:
    from Records.models import *
except ImportError:
    from ...Records.models import *

register = template.Library()


def render_team(team: Team, event: Event) -> str:
    current_quiz = event.get_team_current_quiz(team)
    next_quiz = event.get_team_next_quiz(team)

    values = {
        'rank': event.get_team_rank(team),
        'code': team.short_name,
        'team_name': team.name,
        'score': event.get_team_score(team),
        'current': f"<a href='{current_quiz.get_absolute_url()}'>{current_quiz}</a>",
        'next': f"<a href='{next_quiz.get_absolute_url()}'>{next_quiz}</a>",
        'quizzers': '<br>'.join([str(team) for team in team.get_individuals()]),
        'quizzer_scores': '<br>'.join(
            [str(event.get_individual_score(individual)) for individual in team.get_individuals()]),
    }

    return f"<tr>{''.join([f'<td>{value}</td>' for value in values.values()])}</tr>"


@register.simple_tag()
def ranked_teams_table(event: Event):
    HTML = '''
<table class="table">
    <tr>
        <th>Rank</th>
        <th>Code</th>
        <th>Team Name</th>
        <th>Score</th>
        <th>Current</th>
        <th>Next</th>
        <th>Quizzers</th>
        <th>Score</th>
    </tr>
'''
    HTML += '\n    '.join([render_team(team, event) for team in event.season.get_teams()]) + '\n</table>'

    return format_html(HTML)
