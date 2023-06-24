from django.shortcuts import render, redirect, reverse

try:
    from Records.models import *
except ImportError:
    from ..Records.models import *
from django.utils import timezone

# from .models import ActiveScoreKeepers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Helper methods
def get_quiz_from_scorekeeper_user(user: User) -> Quiz:
    current_individual = Individual.objects.filter(user=user).first()

    if current_individual is None:
        raise AttributeError(
            'You have created an account, but it has not been setup to be a scorekeeper. Please contact your administer to get your account setup.')

    current_quiz = Quiz.objects.filter(scorekeeper=current_individual).filter(isValidated=False).filter(
        round=str(CurrentRound.objects.first().round))

    if current_quiz.exists():
        return current_quiz.first()
    else:
        raise AttributeError(
            "You're all setup, but you haven't been assigned to a quiz. This is probably because the next round hasn't started yet.")


def index(request):
    def render_quiz_as_accordion_item(quiz: Quiz, show: bool = False):
        return f"""
<div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{quiz.room}{quiz.round}" aria-expanded="true" aria-controls="collapse{quiz.room}{quiz.round}">
        {quiz}
      </button>
    </h2>
    <div id="collapse{quiz.room}{quiz.round}" class="accordion-collapse collapse {'show' if show else ''}" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <table>
          <tr>
            <th>Quizmaster</th>
            <td>{quiz.quizmaster}</td>
          </tr>
          <tr>
            <th>Scorekeeper</th>
            <td>{quiz.scorekeeper}</td>
          </tr>
          <tr>
            <th>Teams</th>
            <td>{', '.join([team.name for team in quiz.get_teams()])}</td>
          </tr>
          <tr>
          </tr>
          <tr>
            <td>
              <a href="{quiz.get_uri()}">See more...</a>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
        """

    HTML = f"""
<div class="accordion" id="accordionExample">
    {''.join([render_quiz_as_accordion_item(live_quiz) for live_quiz in sorted(Quiz.objects.filter(event__date__gte=timezone.now().date()), key=lambda q: (1000 * ord(q.room)) + int(q.round))])}
</div>
    """

    return render(request, 'Quiz/index.html', {'quiz_list': HTML})


@login_required
def quiz(request):
    if request.method == 'POST':
        return quiz_backend(request)
    # Find quiz
    # Get questions
    # Get teams
    #     get individuals from teams

    try:
        current_quiz = get_quiz_from_scorekeeper_user(request.user)
    except AttributeError as e:
        return render(request, 'Quiz/quiz.html', {'question_form': e})

    quiz_questions = sorted(current_quiz.get_questions(), key=lambda x: x.question_number)

    NEW_LINE = '\n'

    HTML = f'''\
<form>
<div class="table-div">
    <table>
        <thead>
            <tr>
                <th class="headcol">Quizzer</th> <th></th>   <th class="score-col">Score</th>   {NEW_LINE}{''.join([f'            <th data-question-id="{question.pk}">{question.question_number}</th>{NEW_LINE}' for question in quiz_questions])} 
            </tr>
            <tr>
                <th class="headcol"></th> <th></th>   <th class="score-col"></th>
                {''.join([f'            <th class="not-answered {"""was-not-answered""" if question.ruling == """not answered""" else """"""}" data-question-id="{question.pk}">Not<br>Answered</th>{NEW_LINE}' for question in quiz_questions])} 
            </tr>
        </thead>
    '''

    for team in current_quiz.get_teams():
        HTML += f'        <tbody>{NEW_LINE}'
        HTML += f'          <tr> <th class="headcol team-name">{team.name}</th> <th></th> <th class="score-col team-score"><span class="team-score">0<span></th>  </tr> {NEW_LINE}'

        for team_membership in TeamMembership.objects.filter(team=team):
            quizzer = team_membership.individual
            HTML += f'        <tr>{NEW_LINE}'

            HTML += f'            <th class="headcol individual-name">{quizzer} </th> <td><input data-team-id="{team.pk}" data-quizzer-id="{quizzer.pk}" class="quizzer-validate" type="checkbox"/></td> <td class="score-col individual-score" ></td>   {NEW_LINE}'
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
    </form>
    '''

    return render(request, 'Quiz/quiz.html', {'question_form': HTML})


@login_required
def quiz_backend(request):
    if request.method != 'POST':
        return redirect('quiz')

    # Get quiz
    # Get questions
    # Get teams
    #     get individuals from teams

    try:
        current_quiz = get_quiz_from_scorekeeper_user(request.user)
    except AttributeError as e:
        return HttpResponse(403)

    try:
        current_quizzer = Individual.objects.filter(pk=request.POST.get('quizzer_id')).first()
        current_question = AskedQuestion.objects.filter(pk=request.POST.get('question_id')).first()
        result = request.POST.get('result')
        if any([_ is None for _ in [current_question, result]]):
            raise AttributeError(401)
    except Exception as e:
        if quizzer_id := request.POST.get('quiz_validated_by_quizzer'):
            quizzer = Individual.objects.filter(pk=quizzer_id).first()
            current_quiz.validated_by(quizzer)
        elif request.POST.get('quiz_validated_by_scorekeeper'):
            scorekeeper = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
            current_quiz.validated_by(scorekeeper)

            return HttpResponse(205)

        return HttpResponse(401)

    result_options = {
        'positive': [
            current_quizzer,
            'correct',
            20
        ],
        'negative': [
            current_quizzer,
            'incorrect',
            -10
        ],
        'neutral': [
            None,
            '',
            None
        ],
        'not answered': [
            None,
            'not answered',
            None
        ]
    }

    if result in result_options.keys():
        current_question.individual = result_options[result][0]
        current_question.ruling = result_options[result][1]
        current_question.value = result_options[result][2]
        current_question.save()
        return HttpResponse(200)
    else:
        return HttpResponse(401)
