from django.test import TestCase
from django.urls import reverse
from .models import Note
from .forms import NoteForm


# tests for the note model
class NoteModelTest(TestCase):
    def setUp(self):
        Note.objects.create(
            title="Elden Ring boss order",
            content="Margit, Godrick, Rennala, Radahn",
        )

    def test_note_has_title(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, "Elden Ring boss order")

    def test_note_has_content(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, "Margit, Godrick, Rennala, Radahn")

    def test_note_str_returns_title(self):
        note = Note.objects.get(id=1)
        self.assertEqual(str(note), "Elden Ring boss order")

    def test_created_at_auto_set(self):
        note = Note.objects.get(id=1)
        self.assertIsNotNone(note.created_at)


# tests for the note form
class NoteFormTest(TestCase):
    def test_valid_form(self):
        form = NoteForm(data={
            "title": "backlog",
            "content": "Hollow Knight, Silksong, Hades 2",
        })
        self.assertTrue(form.is_valid())

    def test_missing_title_invalid(self):
        form = NoteForm(data={"title": "", "content": "no title"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_missing_content_invalid(self):
        form = NoteForm(data={"title": "no content", "content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


# tests for the views (covers all CRUD url patterns)
class NoteViewTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="raid night",
            content="Destiny 2 at 8pm",
        )

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "raid night")

    def test_note_detail_view(self):
        response = self.client.get(
            reverse("note_detail", args=[self.note.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "raid night")
        self.assertContains(response, "Destiny 2 at 8pm")

    def test_note_detail_404_for_missing(self):
        response = self.client.get(reverse("note_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_note_create_get(self):
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_note_create_post_adds_note(self):
        response = self.client.post(reverse("note_create"), {
            "title": "new game",
            "content": "Baldurs Gate 3 run",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="new game").exists())

    def test_note_update_post_changes_note(self):
        response = self.client.post(
            reverse("note_update", args=[self.note.id]),
            {"title": "raid night (moved)", "content": "9pm now"},
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "raid night (moved)")
        self.assertEqual(self.note.content, "9pm now")

    def test_note_delete_removes_note(self):
        response = self.client.get(
            reverse("note_delete", args=[self.note.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
