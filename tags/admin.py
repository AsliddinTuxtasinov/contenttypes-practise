from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import TaggedItem


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    # inlines = [TaggedItemInline]
    # list_display = ["title", "is_published"]
    readonly_fields = ["content_object"]
