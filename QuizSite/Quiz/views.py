from django.shortcuts import render, redirect
from Records.models import Quiz, AskedQuestion, Team, TeamMembership, Individual, User
from .models import ActiveScoreKeepers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Helper methods
def get_quiz_from_scorekeeper_user(user: User) -> Quiz:
    current_individual = Individual.objects.filter(user=user).first()

    if current_individual is None:
        raise AttributeError(
            'You have created an account, but it has not been setup to be a scorekeeper. Please contact your administer to get your account setup.')

    current_scorekeeper = ActiveScoreKeepers.objects.filter(scorekeeper=current_individual).first()

    if current_scorekeeper is None:
        raise AttributeError(
            "You're all setup, but you haven't been assigned to a quiz. This is probably because the next round hasn't started yet.")

    return current_scorekeeper.quiz


def index(request):
    return render(request, 'Quiz/index.html')


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

    NEW_LINE = '\n'

    HTML = f'''\
<form>
<div class="table-div">
    <table>
        <thead>
            <tr>
                <th class="headcol">Quizzer</th>   <th class="score-col">Score</th>   {NEW_LINE}{''.join([f'            <th>{_}</th>{NEW_LINE}' for _ in range(1, len(current_quiz.get_questions()) + 1)])} 
            </tr>
            <tr>
                <th class="headcol"></th>   <th class="score-col"></th>   {NEW_LINE}{''.join([f'            <th class="not-answered invisible">Not Answered</th>{NEW_LINE}' for _ in range(1, len(current_quiz.get_questions()) + 1)])} 
            </tr>
        </thead>
    '''

    for team in current_quiz.get_teams():
        HTML += f'        <tbody>{NEW_LINE}'
        HTML += f'          <tr> <th class="headcol team-name">{team.name}</th> <th class="score-col team-score"><span class="team-score">0<span></th>  </tr> {NEW_LINE}'

        for team_membership in TeamMembership.objects.filter(team=team):
            quizzer = team_membership.individual
            HTML += f'        <tr>{NEW_LINE}'

            HTML += f'            <th class="headcol individual-name">{quizzer}</th> <td class="score-col individual-score" ></td>   {NEW_LINE}'
            for question in sorted(current_quiz.get_questions(), key=lambda x: x.question_number):
                # Create checkbox span things per question
                span_class = 'checkbox-img '

                if question.individual == quizzer:

                    if question.ruling == 'correct':
                        span_class += 'positive'
                    elif question.ruling == 'incorrect':
                        span_class += 'negative'

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
        if any([_ is None for _ in [current_quizzer, current_question, result]]):
            raise AttributeError(401)
    except Exception as e:
        return HttpResponse(401)

    print(current_quizzer, current_question, result)

    if result == 'positive':
        current_question.individual = current_quizzer
        current_question.ruling = 'correct'
        current_question.value = 20
        current_question.save()
        print(current_quizzer, current_question, result, '')

        return HttpResponse(200)

    elif result == 'negative':
        current_question.individual = current_quizzer
        current_question.ruling = 'incorrect'
        current_question.value = -10
        current_question.save()
        print(current_quizzer, current_question, result, '')

        return HttpResponse(200)

    elif result == 'neutral':

        current_question.individual = None
        current_question.ruling = ''
        current_question.value = None
        current_question.save()
        print(current_quizzer, current_question, result, '')

        return HttpResponse(200)

    else:
        return HttpResponse(401)
