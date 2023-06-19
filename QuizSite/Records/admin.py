from django.contrib import admin

# Register your models here.


from .models import Organization, Team, Individual, Season, Event, Quiz, AskedQuestion, League, QuizParticipants, \
    TeamMembership, LeagueMembership

admin.site.register(League)
admin.site.register(Season)
admin.site.register(Organization)

admin.site.register(Team)
admin.site.register(Individual)

admin.site.register(Event)
admin.site.register(Quiz)
admin.site.register(AskedQuestion)

admin.site.register(QuizParticipants)
admin.site.register(TeamMembership)
admin.site.register(LeagueMembership)
