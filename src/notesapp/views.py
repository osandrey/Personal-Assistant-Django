from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, NoteForm, NoteSearchForm
from .models import Tag, Note


@login_required
def search_note(request):
    form = NoteSearchForm(request.GET)
    keyword = request.GET.get('keyword', None)
    notes = Note.objects.filter(user=request.user).all()
    if keyword:
        notes = notes.filter(title__icontains=keyword) | notes.filter(description__icontains=keyword)
    return render(request, 'search_note.html', {'form': form, 'notes': notes})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='usersapp:main')
        else:
            return render(request, 'notesapp/add_tag.html', context={'form': form})

    return render(request, 'notesapp/add_tag.html', context={'form': TagForm()})


@login_required
def add_note(request):
    tags = Tag.objects.filter(user=request.user).all()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags:
                note.tags.add(tag)
            return redirect(to='usersapp:main')
        else:
            return render(request, 'notesapp/add_note.html',  context={'form': form, 'tags': tags})

    return render(request, 'notesapp/add_note.html', context={'form': NoteForm(), 'tags': tags})


@login_required
def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'notesapp/detail_note.html', context={"note": note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect(to="#")
    return render(request, 'notesapp/delete_note.html', {'note': note})


@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    tags = note.tags.all()

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            note.tags.set(tags)
            return redirect(to="#", note_id=note_id)
        else:
            return render(request, 'notesapp/update_note.html', context={'form': form})

    return render(request, 'notesapp/update_note.html',
                  context={'form': NoteForm(instance=note), 'note_id': note_id})


