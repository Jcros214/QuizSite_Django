from django.shortcuts import render
from Records.models import Quiz, AskedQuestion, Team, TeamMembership, Individual


# Create your views here.

def index(request):
    return render(request, 'Quiz/index.html')


def quiz(request):
    # Find quiz
    # Get questions
    # Get teams
    #     get individuals from teams

    current_quiz = Quiz.objects.get(pk=1)

    NEW_LINE = '\n'

    HTML = f'''\
<form>
    <div class="table-div">
    <table>
        <tr>
            <td>Quizzer</td>{NEW_LINE}{''.join([f'            <td>{_}</td>{NEW_LINE}' for _ in range(1, len(current_quiz.get_questions()) + 1)])} 
        </tr>
    '''

    for team in current_quiz.get_teams():
        # How do you separate the teams?

        for quizzer in TeamMembership.objects.filter(team=team):
            HTML += f'        <tr>{NEW_LINE}'

            HTML += f'            <td>{quizzer}</td>{NEW_LINE}'
            for question in current_quiz.get_questions():
                # Create checkbox span things per question
                HTML += f'            <td><span class="checkbox-img" style="height:25px;"></span></td>{NEW_LINE}'

            HTML += '        </tr>\n'

    HTML += '''\
        </table>
        </div>
    </form>
    '''

    return render(request, 'Quiz/quiz.html', {'question_form': HTML})
