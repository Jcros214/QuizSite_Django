from django.contrib import admin
from nonrelated_inlines.admin import NonrelatedTabularInline

# Register your models here.


from .models import *

admin.site.register(League)
admin.site.register(Season)
admin.site.register(Organization)

admin.site.register(Team)
admin.site.register(Individual)

admin.site.register(Quiz)
admin.site.register(AskedQuestion)

admin.site.register(QuizParticipants)
admin.site.register(TeamMembership)
admin.site.register(LeagueMembership)
admin.site.register(CurrentRound)


class IndividualInline(NonrelatedTabularInline):
    model = Individual
    extra = 0

    def get_form_queryset(self, obj):
        # Filter to only individuals who are part of teammemberships with teams that are part of the current season
        return self.model.objects.filter(teammembership__team__season=obj.season)

    def save_new_instance(self, parent, instance):
        ...  # don't


class EventAdmin(admin.ModelAdmin):
    inlines = [IndividualInline]


admin.site.register(Event, EventAdmin)
