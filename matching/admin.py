from django.contrib import admin
from .models import MatchingEntry

class MatchingEntryAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'album_macrogenre')

    def user_username(self, obj):
        return obj.user.username

admin.site.register(MatchingEntry, MatchingEntryAdmin)
