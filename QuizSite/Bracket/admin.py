from django.contrib import admin
from .models import Team, Match, Bracket


# Register your models here.

@admin.register(Bracket)
class BracketAdmin(admin.ModelAdmin):
    ...


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_match', 'children', 'bracket',
                    'round', 'team1', 'team2', 'team1_points', 'team2_points')

    def name(self, obj):
        return str(obj)

    def children(self, obj):
        return Match.objects.filter(parent_match=obj)
