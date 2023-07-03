from typing import Any, Dict
from .models import Match, Bracket, Team
from .forms import TeamCreateForm, TeamEditForm, BracketForm, TeamBracketForm
from django.forms import formset_factory
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
import math


# Bracket views


#   List view
class BracketListView(ListView):
    model = Bracket
    template_name = "Bracket/bracket_list.html"


#   Item view
class BracketEditView(DetailView):
    model = Bracket
    template_name = "Bracket/bracket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["round_list"] = [
            Match.objects.filter(bracket=self.object.pk, round=round_num)
            for round_num in range(1, 5)
        ]

        return context


#   Create view
class BracketCreateView(FormView):
    form_class = BracketForm
    # fields = ["name", "num_teams"]
    template_name = "Bracket/bracket_create.html"

    def get_success_url(self):
        return reverse("bracket:bracket_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        TeamBracketFormSet = formset_factory(TeamBracketForm, extra=16)
        formset = TeamBracketFormSet()

        context["formset"] = formset
        context["teams"] = Team.objects.all()

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        num_teams = int(form.cleaned_data["num_teams"])

        TeamFormSet = formset_factory(TeamBracketForm, extra=16)
        formset = TeamFormSet(self.request.POST)

        if formset.is_valid():
            formset_seed_dict = {seed: form.cleaned_data["team"] for seed, form in enumerate(formset)}

            match_up_sets = self.generate_bracket(num_teams)

            # Teams
            teams = []
            for match_up in match_up_sets:
                for team in match_up:
                    teams.append(Team.objects.get(pk=formset_seed_dict[team - 1].pk))

            # Create Matches
            Bracket.create_with_matches(teams, form.cleaned_data["name"])
        return super().form_valid(form)

    @staticmethod
    def generate_bracket(num_teams):
        if num_teams not in (4, 8, 16, 32, 64):
            raise ValueError("Number of teams must be a value in the set 4, 8, 16, 32, 64")

        bracket = [(i + 1, num_teams - i) for i in range(num_teams // 2)]
        bracket = [bracket[i // 2] if i % 2 == 0 else bracket[-(i // 2) - 1] for i in range(len(bracket))]

        bracket_dict = {}

        for ind, highest in enumerate(bracket[::2]):
            bracket_dict[highest[0]] = bracket[2 * ind:2 * ind + 2]

        sorted_list = sorted(bracket_dict.keys())
        sorted_keys = []

        while sorted_list:
            sorted_keys.insert(math.ceil(len(sorted_keys) / 2), sorted_list.pop(0))

        output = []

        for key in sorted_keys:
            [output.append(bracket_dict[key][_]) for _ in range(2)]

        return output


# Team views

#   List view
class TeamListView(ListView):
    model = Team
    template_name = "Bracket/team_list.html"


#   Item view
class TeamEditFormView(FormView):
    template_name = "Bracket/team.html"
    form_class = TeamEditForm

    def get_success_url(self) -> str:
        return reverse("bracket:team_list")  # , kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        team = Team.objects.get(pk=self.kwargs["pk"])
        team.name = form.cleaned_data["team"]
        team.save()

        return super().form_valid(form)

    def form_invalid(self, form: Any) -> HttpResponse:
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = get_object_or_404(Team, pk=self.kwargs["pk"])

        return context


#   Create view
class TeamCreateFormView(FormView):
    template_name = "Bracket/team_create.html"
    form_class = TeamCreateForm

    def get_success_url(self) -> str:
        return reverse("bracket:team_list")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        Team.objects.create(name=form.cleaned_data["name"])

        if self.request.POST.get('submit_and_add_another'):
            return redirect(reverse("bracket:team_create"))

        return super().form_valid(form)


# DB Endpoints
def update_match_score(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        match, team, score = [int(request.POST.get(key, 0)) for key in ["match", "team", "score"]]
    except ValueError:
        return HttpResponse(status=400, content='user misclick; ignore', content_type='text/plain')

    match = Match.objects.get(pk=match)
    team = Team.objects.get(pk=team)
    # score = int(score)

    result = match.update_score(team, score)

    if result is not None:
        if result == "refresh":
            return HttpResponse(status=205, content=result, content_type="text/plain")
        return HttpResponse(status=400, content=result, content_type="application/json")

    return HttpResponse(status=204)
