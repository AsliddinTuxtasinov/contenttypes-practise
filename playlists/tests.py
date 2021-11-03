from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from test_projects.db.models import PublishStateOptions
from .models import Playlist


class PlaylisttModelTestCase(TestCase):

    # vaqtinchalik test uchun test object yaratish
    def setUp(self):
        self.obj_a = Playlist.objects.create(title="bu title fieldi")
        self.obj_b = Playlist.objects.create(title="bu title fiel", state=PublishStateOptions.PUBLISH)

    # slugni test qilish
    def test_slug_field(self):
        title = self.obj_a.title
        title_slug = slugify(title)
        self.assertEqual(title_slug, self.obj_a.slug)

    # titile kiritilganini test qilish
    def test_valid_title(self):
        title = "bu title fieldi"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())

    # Playlist yaratilganini test qilish
    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)

    # draftni test qilish playlist
    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    # publish va publish_timestampni test qilish playlist
    def test_publish_case(self):
        now = timezone.now()
        qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(qs.exists())

    # publishni test qilish playlist
    def test_publish_manager(self):
        qs = Playlist.objects.all().published()
        qs2 = Playlist.objects.published()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), qs2.count())
