from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, NoteForm
from .models import Tag, Note
from django.db import models


@login_required
def search_note(request):
    search_query = request.GET.get('search_query', '')
    user_notes = Note.objects.filter(user=request.user)
    search_results = user_notes.filter(
        models.Q(title__icontains=search_query) |
        models.Q(description__icontains=search_query)
    )

    context = {
        'search_query': search_query,
        'search_results': search_results
    }

    return render(request, 'notesapp/search_note.html', context)


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
        return redirect(to='usersapp:main')
    return render(request, 'notesapp/delete_note.html', {'note': note})


@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags:
                note.tags.add(tag)
            return redirect(to='usersapp:main', note_id=note_id)
        else:
            return render(request, 'notesapp/update_note.html', context={'form': form})

    return render(request, 'notesapp/update_note.html',
                  context={'form': NoteForm(instance=note), 'note_id': note_id})


