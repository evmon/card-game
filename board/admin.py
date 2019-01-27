from django.contrib import admin

from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
	list_display = ['info', 'id', 'created_at',]
