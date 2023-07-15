from django import template
from django.urls import reverse
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
        # 'quizzer_scores': '<br>'.join(
        #     [str(event.get_individual_score(individual)) for individual in team.get_individuals()]),
    }

    return f"<tr>{''.join([f'<td>{value}</td>' for value in values.values()])}</tr>"


@register.simple_tag()
def ranked_teams_table(event: Event):
    print("started trying to get data")

    data = event.get_event_view_data()

    print("successfully got data")

    caches = {}

    html = '<table class="table">'

    division = None

    prv_score = None

    for team in data:
        if team['division'] != division:
            color = 'danger' if team['division'] == 'R' else 'primary'
            close_tag = '</tbody>' if division is not None else ''
            html += f'{close_tag}<tbody class="table-{color}">'
            html += '''
                <tr>
        <th>Rank</th>
        <th>Code</th>
        <th>Team Name</th>
        <th>Score</th>
        <th>Current</th>
        <th>Next</th>
        <th>Quizzers</th>
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

            current_round_repr = f"{current_round_object}"

            current_round = f"<a href='{current_round_object.get_absolute_url()}'>{current_round_repr}</a>"
        else:
            current_round = "None"

        next_round_object = Quiz.objects.filter(pk=team['next_round'])
        if next_round_object.exists():
            next_round_object = next_round_object.first()
            next_round = f"<a href='{next_round_object.get_absolute_url()}'>{next_round_object}</a>"
        else:
            next_round = "None"

        html += "\n<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>".format(
            team['rank'],
            team['code'],
            team['name'],
            team['score'],
            current_round,
            next_round,
            '<br>'.join([str(quizzer['name']) for quizzer in team['individuals']]),
        )

        prv_score = team['score']

    html += '\n</table>'

    html += f'''
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

    return format_html(html)


#

def render_quiz(quiz: Quiz) -> str:
    return f"<a href='{quiz.get_absolute_url()}'>{quiz.room}{quiz.round}</a>"


def render_team_row(team: dict) -> str:
    current_round_object = Quiz.objects.filter(pk=team['current_round'])
    if current_round_object.exists():
        team['current_quiz_string'] = render_quiz(current_round_object.first())

    next_round_object = Quiz.objects.filter(pk=team['next_round'])
    if next_round_object.exists():
        team['next_quiz_string'] = render_quiz(next_round_object.first())

    html = f"""
         <tr>
             <td>{team['rank']}</td>
             <td>{team['code']}</td>
             <td>{team['name'].replace(' ', '&nbsp;')}</td>
             <td>{team['score']}</td>
            <td>{team.get('current_quiz_string', ' -- ')}</td>
            <td>{team.get('next_quiz_string', ' -- ')}</td>
             <td>
                 {' / '.join([str(quizzer['name']) for quizzer in team['individuals']]).replace(' ', '&nbsp;')}
             </td>
         </tr>
         """
    return html


division_colors = {
    'R': 'danger',
    'B': 'primary',
}


def render_division_table(division_data: list[dict], division: Division = None) -> str:
    caches = {}
    prv_score = None

    division_letter = division.name if division is not None else ''

    color = division_colors.get(division_letter, '')

    html = f'''
<table class="table table-sm table-{color}">
    <thead>
        <tr>
            <th>Rank</th>
            <th>Code</th>
            <th>Team Name</th>
            <th>Score</th>
            <th>Current Round</th>
            <th>Next Round</th>
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
    #
    #         prv_score = team['score']
    #
    #      f'''
    #     <tr>
    #         <td style="height: 82px;"></td>
    #         <td></td>
    #         <td></td>
    #         <td></td>
    #         <td></td>
    #         <td></td>
    #         <td></td>
    #     </tr>
    #     </tbody>
    #     <thead>
    #         <tr>
    #             <th>Division</th>
    #             <th></th>
    #             <th>Minimum Points</th>
    #             <th></th>
    #             <th></th>
    #             <th></th>
    #             <th></th>
    #         </tr>
    #         <tr>
    #             <td>Championship</td>
    #             <td></td>
    #             <td>{caches.get('champ', 'N/A')}</td>
    #             <th></th>
    #             <th></th>
    #             <td></td>
    #             <td></td>
    #
    #         </tr>
    #         <tr>
    #             <td>Consolation 1</td>
    #             <td></td>
    #             <td>{caches.get('cons1', 'N/A')}</td>
    #             <th></th>
    #             <th></th>
    #             <td></td>
    #             <td></td>
    #         </tr>
    #     </thead>
    # </table>
    # '''
    return html


def render_a_division_table(division: Division) -> str:
    data = division.get_division_view_data()

    return format_html(render_division_table(data, division))


@register.simple_tag(takes_context=True)
def live_event(context):
    event = context['event']
    data = event.get_event_view_data()

    divisions = [
        [team for team in data if team['division'] == 'Blue'],
        [team for team in data if team['division'] == 'Red'],
    ]

    html = f'''
    
    <div class="row" style="height: calc(100vh - 40px); width: calc(100vw - 40px);">
    
        {''.join([f'<div class="col-md-6">{render_division_table(division)}</div>' for division in divisions])}
    
    </div>
    
    '''
    return format_html(html)


@register.simple_tag(takes_context=True)
def live_division(context):
    division = context['division']
    data = division.get_division_view_data()

    html = f'''
        <div class="division-table division-red" hx-get="{reverse('records:live_division_display_table', kwargs={'division_id': division.id})}"
         hx-trigger="every 2s">
            {render_division_table(data, division)}
        </div>
    '''
    return format_html(html)
