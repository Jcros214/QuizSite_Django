from django import template
from django.utils.html import format_html
from Bracket.models import Match, Bracket

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def first_half(value):
    if len(value) == 1:
        return value
    return value[:(len(value) // 2)]


@register.filter
def second_half(value):
    return value[(len(value) // 2):]


@register.filter
def except_last(value):
    return value[:-1]


@register.simple_tag()
def render_match(match: Match, added_classes: str = ""):
    if not isinstance(match, Match):
        raise TypeError(f"Expected Match, got {type(match)}")

    team_data = [{}, {}]

    positions = ['top', 'bottom']

    for ind, team in enumerate([match.team1, match.team2]):
        if team is not None:
            team_data[ind]["team"] = team
            team_data[ind]["pk"] = team.pk
            team_data[ind]["points"] = match.get_points(team)
            team_data[ind]["added_classes"] = '' if (win_loss := match.get_win_loss(
                team)) is None else 'winner' if win_loss else 'loser'
        team_data[ind]["added_classes"] = team_data[ind].get("added_classes", '') + ' ' + positions.pop(0)

    output = []

    for team in team_data:
        output.append(f'''
        <div class="team {team.get('added_classes', '')}">
            <span class="rank">{match.get_rank(team.get('team'))}</span>&nbsp;&nbsp;{team.get('team', '')}&nbsp;&nbsp;<span class="score" data-match="{match.pk}" data-team="{team.get('pk', '')}" 
            contenteditable="true">{team.get('points', '')}</span>&nbsp;&nbsp;
        </div>
        ''')

    output = '<div class="team-spacer"></div>'.join(output)

    output = f'<div class="match {added_classes}"> {output} </div>'

    return format_html(output)


@register.simple_tag()
def render_bracket(bracket: Bracket):
    matches = Match.objects.filter(bracket=bracket)
    num_rounds = max([match.round for match in matches]) + 1
    rounds = [[] for _ in range(num_rounds)]

    # For each match,
    #   if it has no children, add it to the first round,

    #   while it has a parent, (i.e. it's not the final match)
    #       try to add it's parent to the next round

    for match in matches:
        if match.round == 1:
            rounds[0].append(match)
            while match.parent_match:
                parent_match = match.parent_match
                if parent_match not in rounds[parent_match.round - 1]:
                    rounds[parent_match.round - 1].append(parent_match)
                match = parent_match

    # sort matches pairs by their .is_upper_child attribute

    def convert_to_pairs_array(lst):
        pairs = []
        for i in range(0, len(lst), 2):
            pairs.append(lst[i:i + 2])
        return pairs

    rounds_copy = [[] for _ in range(num_rounds)]

    for ind, round in enumerate(rounds):
        for child_pair in convert_to_pairs_array(round):
            [rounds_copy[ind].append(match) for match in
             sorted(child_pair, key=lambda x: x.is_upper_child, reverse=True)]

    rounds = rounds_copy

    HTML = '<div class="tournament">'

    for round_num, round in enumerate(rounds[:-1]):
        HTML += f'<div class="round round-{len(rounds) - round_num - 2}">'
        half_round = round[:len(round) // 2] if len(round) != 1 else round
        for match in half_round:
            final_class = 'final' if len(rounds) - round_num - 2 == 0 else ''
            HTML += render_match(match, f'left {final_class}')
        HTML += '</div>'
    for round_num, round in enumerate(reversed(rounds[:-2])):
        HTML += f'<div class="round round-{round_num + 1}">'
        half_round = round[len(round) // 2:] if len(round) != 1 else round
        for match in half_round:
            HTML += render_match(match, 'right')
        HTML += '</div>'
    HTML += '</div>'
    return format_html(HTML)
