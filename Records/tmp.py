from Records.models import Team, TeamMembership, Individual

[[TeamMembership(team = Team.objects.get(id=((__ - 6) / 2)), individual=Individual.objects.get(id=__)) for __ in _] for _ in zip(range(7,79,2),range(8,79,2))]