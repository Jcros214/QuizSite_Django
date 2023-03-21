from django.contrib import admin

# Register your models here.


from .models import Orginization, Team, Individual, Season, Event, Quiz, AskedQuestion

admin.site.register(Season)
admin.site.register(Orginization)

admin.site.register(Team)
admin.site.register(Individual)

admin.site.register(Event)
admin.site.register(Quiz)
admin.site.register(AskedQuestion)
