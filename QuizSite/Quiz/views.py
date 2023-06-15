from django.shortcuts import render
from Records.models import Quiz, AskedQuestion, Team, TeamMembership, Individual


# Create your views here.

def index(request):
    return render(request, 'Quiz/index.html')


def quiz(request):
    return render(request, 'Quiz/quiz.html')


# Find quiz
# Get questions
# Get teams
#     get individuals from teams

"""

<form>
    
    <table>
        <tr>
            <th>Quizzer</th>
            {% for question in questions %}
                <th>{{question.number}}</th>
            {% endfor %}
        <tr>
            <td>{{Quizzer}}</td>
            {% for question in questions %}
                <td>{{quizzer result per question}}</td>
            {% endfor %}
        </tr>
    </table>

</form>


"""

HTML = ''

# current_quiz = Quiz.objects.get(pk=1)
#
# for team in current_quiz.getTeams():
#     for quizzer in team:
#         for question in current_quiz.getQuestions():
#             ...
