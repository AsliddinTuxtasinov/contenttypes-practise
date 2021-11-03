from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from test_projects.db.models import PublishStateOptions
from test_projects.db.receivers import slugify_save, published_state_save

from tags.models import TaggedItem


class PlaylistManagerQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now)


class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistManagerQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    tags = GenericRelation(TaggedItem, related_query_name="playlist")

    objects = PlaylistManager()

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.active

    @property
    def all_tags(self):
        return ', '.join(str(i) for i in self.tags.all())


pre_save.connect(slugify_save, sender=Playlist)
pre_save.connect(published_state_save, sender=Playlist)
