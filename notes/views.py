from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from .models import Note

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