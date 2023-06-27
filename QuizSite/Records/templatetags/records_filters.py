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
    data = event.get_event_view_data()

    caches = {}

    HTML = '<table class="table">'

    division = None

    prv_score = None

    for team in data:
        if team['division'] != division:
            color = 'danger' if team['division'] == 'R' else 'primary'
            close_tag = '</tbody>' if division is not None else ''
            HTML += f'{close_tag}<tbody class="table-{color}">'
            HTML += '''
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

            division = team['division']

        if team['rank'] > 6 and caches.get(team['division'] + 'champ') is None:
            caches[team['division'] + 'champ'] = prv_score
        elif team['rank'] > 12 and caches.get(team['division'] + 'champ') is None:
            caches[team['division'] + 'cons1'] = prv_score

        current_round_object = Quiz.objects.filter(pk=team['current_round'])
        if current_round_object.exists():
            current_round_object = current_round_object.first()
            current_round = f"<a href='{current_round_object.get_absolute_url()}'>{current_round_object}</a>"
        else:
            current_round = "None"

        next_round_object = Quiz.objects.filter(pk=team['next_round'])
        if next_round_object.exists():
            next_round_object = next_round_object.first()
            next_round = f"<a href='{next_round_object.get_absolute_url()}'>{next_round_object}</a>"
        else:
            next_round = "None"

        HTML += "\n<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>".format(
            team['rank'],
            team['code'],
            team['name'],
            team['score'],
            current_round,
            next_round,
            '<br>'.join([str(quizzer['name']) for quizzer in team['individuals']]),
            '<br>'.join([str(quizzer['score']) for quizzer in team['individuals']]))

        prv_score = team['score']

    HTML += '\n</table>'

    HTML += f'''
    <h3>Points to get into a bracket</h3>
    <table class="table">
        <tr>
            <th>Division</th>
            <th>Points</th>
        </tr>
        <tr class="table-primary">
            <td>Blue - Championship</td>
            <td>{caches.get('B' + 'champ')}</td>
        </tr>
        <tr class="table-primary">
            <td>Blue - Consolation 1</td>
            <td>{caches.get('B' + 'cons1')}</td>
        </tr>
        <tr class="table-danger">
            <td>Red - Championship</td>
            <td>{caches.get('R' + 'champ')}</td>
        </tr>
        <tr class="table-danger">
            <td>Red - Consolation 1</td>
            <td>{caches.get('R' + 'champ')}</td>
        </tr>

        </table>
            
            
    
    '''

    return format_html(HTML)
