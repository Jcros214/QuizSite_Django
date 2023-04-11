# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Records.models import League, Season, Event, Quiz, AskedQuestion, Orginization, Team, TeamMembership, Individual


# Orginization, Team, TeamMembership, Individual, Event


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = []


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = []


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = []


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = []


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AskedQuestion
        fields = []