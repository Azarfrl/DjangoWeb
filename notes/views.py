from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from .models import Note
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
    else:
        notes = []  

    form = NoteForm()  

    return render(request, 'notes/home.html', {
        'form': form,
        'notes': notes,
        'is_authenticated': request.user.is_authenticated,
    })

@login_required  
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  
            note.save()
            return redirect('home')
    else:
        form = NoteForm()

    return render(request, 'notes/add_note.html', {'form': form})  

@login_required
@require_POST
def update_note(request, note_id):          
    note = get_object_or_404(Note, id=note_id, user=request.user)
    content = request.POST.get('content', '').strip()
    if not content:
        messages.error(request, "Note cannot be empty.")
    else:
        note.content = content
        note.save()
        messages.success(request, "Note updated.")
    return redirect('home')

@login_required
@require_POST
def delete_note(request, note_id):         
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect('home')