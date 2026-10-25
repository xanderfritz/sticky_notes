from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm


# list all notes
def note_list(request):
    notes = Note.objects.all()
    context = {
        "notes": notes,
        "page_title": "my sticky notes",
    }
    return render(request, "notes/note_list.html", context)


# single note page
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


# new note
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form})


# edit a note
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form})


# delete a note
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect("note_list")
