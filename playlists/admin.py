from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["title", "is_published"]
    readonly_fields = ["publish_timestamp", "all_tags"]
