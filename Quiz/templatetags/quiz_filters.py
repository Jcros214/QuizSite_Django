from django import template
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html

try:
    from Records.models import *
except ImportError:
    from ...Records.models import *

register = template.Library()


@register.filter('has_group')
def has_group(user: User, group_name):
    groups = user.groups.all().values_list('name', flat=True)

    return True if (group_name in groups or user.is_superuser) else False


@register.simple_tag(name='display_official_schedule', takes_context=True)
def display_official_schedule(context):
    request = context['request']
    active_user: User = request.user

    # Get active events
    active_events = Event.objects.filter(date=timezone.now().date())

    # Get all quizzes from active_events where active user is an official

    try:
        Individual.objects.get(user__username=active_user.username)
    except Individual.DoesNotExist:
        return format_html('<p>You are not an official, and I\'m not sure how you got here...</p>')

    event_quizzes = Quiz.objects.filter(event__in=active_events)

    quizzes = event_quizzes.filter(quizmaster=active_user) | event_quizzes.filter(scorekeeper=active_user)

    pass


@register.simple_tag(name='render_scoresheet')
def render_scoresheet(quiz: Quiz, mutable=True):
    current_quiz = quiz
    if not isinstance(current_quiz, Quiz):
        return "It looks like you haven't been assigned to any more quizzes. If you think this is a mistake, please reach out to your administers."

    quiz_questions = current_quiz.get_questions().order_by('question_number')

    NEW_LINE = '\n'

    HTML = f'''\
    <form>
    <div class="table-div">
        <table>
            <thead>
                <tr>
                    <th class="headcol">Quizzer</th> <th></th>   <th class="score-col">Score</th>   
                    {''.join([f'            <th class="question-number" data-question-id="{question.pk}">{question.question_number}</th>{NEW_LINE}' for question in quiz_questions])} 
                </tr>
                <tr>
                    <th class="headcol"></th> <th></th>   <th class="score-col"></th>
                    {''.join([f'            <th class="not-answered {"""was-not-answered""" if question.ruling == """not answered""" else ("""""" if mutable else """invisible""")}" data-question-id="{question.pk}">Not<br>Answered</th>{NEW_LINE}' for question in quiz_questions])} 
                </tr>
            </thead>
        '''

    for team in current_quiz.get_teams():
        if False and mutable:
            team_name_select = '<select class="team-select">'
            for selectable_team in Team.objects.filter(season=current_quiz.event.season).order_by('name'):
                team_name_select += f'<option value="{selectable_team.pk}" {"selected" if selectable_team == team else ""}>{selectable_team.name} - {selectable_team.short_name}</option>'
            team_name_select += '</select>'
        else:
            team_name_select = team.name
        HTML += f'        <tbody>{NEW_LINE}'
        HTML += f'          <tr> <th class="headcol team-name">{team_name_select}</th> <th></th> <th class="score-col team-score"><span class="team-score">{current_quiz.get_team_results(team)}<span></th>  </tr> {NEW_LINE}'

        for team_membership in TeamMembership.objects.filter(team=team):
            quizzer = team_membership.individual
            HTML += f'        <tr>{NEW_LINE}'

            if mutable:
                validate_box = f'<input data-team-id="{team.pk}" data-quizzer-id="{quizzer.pk}" class="quizzer-validate" type="checkbox"/>'
            else:
                validate_box = ''

            HTML += f'            <th class="headcol individual-name">{quizzer} </th> <td>{validate_box}</td> <td class="score-col individual-score" ></td>   {NEW_LINE}'
            for question in quiz_questions:
                # Create checkbox span things per question
                span_class = 'checkbox-img '

                if question.individual == quizzer:

                    if question.ruling == 'correct':
                        span_class += 'positive'
                    elif question.ruling == 'incorrect':
                        span_class += 'negative'
                    elif question.ruling == 'not answered':
                        ...  # Handled above

                HTML += f'            <td class="question-td"><span data-quizzer-id="{quizzer.pk}" data-question-id="{question.pk}" class="{span_class}" style="min-height:25px;"></span></td>{NEW_LINE}'

            HTML += '        </tr>\n'
        HTML += '        </tbody>\n'

    HTML += '''\
            </table>
        </div>
        '''
    if mutable:
        HTML += '''
        <div class="button-div"  style="margin-top: 70px">
            <button id="submit" class="btn btn-primary" disabled>Submit Scores</button>
            <button id="tiebreaker" class="btn btn-secondary" disabled>Add Tiebreaker</button>
        </div>
        '''
    HTML += '</form>'

    return format_html(HTML)
