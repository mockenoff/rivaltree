from django.contrib import admin

from apps.bracketr import models

admin.site.register(models.Bracket)
admin.site.register(models.Team)
admin.site.register(models.Game)
