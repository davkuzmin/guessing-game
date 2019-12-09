from django.contrib import admin

from .models import *


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Guess)
class GuessAdmin(admin.ModelAdmin):
    pass
