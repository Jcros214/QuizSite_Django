from django import forms
from .models import Team


class TeamCreateForm(forms.Form):
    name = forms.CharField(max_length=100)


class TeamEditForm(forms.Form):
    name = forms.CharField(max_length=100)


class TeamBracketForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    seed = forms.IntegerField(min_value=1, max_value=64)


class BracketForm(forms.Form):
    name = forms.CharField(max_length=100)
    num_teams = forms.ChoiceField(choices=[(2 ** i, 2 ** i) for i in range(2, 7)])

