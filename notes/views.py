from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note

def home(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm()

    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/home.html', {'form': form, 'notes': notes})