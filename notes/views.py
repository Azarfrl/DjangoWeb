from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NoteForm, SubjectForm, SubjectImage
from .models import Note, Subject, SubjectImage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')     
    return render(request, 'notes/home.html', {'form': NoteForm()})

@login_required
def add_note(request, subject_id=None):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            
            if subject_id:                          
                subject = get_object_or_404(Subject, id=subject_id, user=request.user)
                note.subject = subject
                note.save()
                return redirect('subject_notepad', subject_id=subject.id)
            else:
                note.save()
                return redirect('dashboard')

    return redirect('dashboard')

@login_required
def update_note(request, note_id):          
    note = get_object_or_404(Note, id=note_id, user=request.user)
    content = request.POST.get('content', '').strip()
    if not content:
        messages.error(request, "Note cannot be empty.")
    else:
        note.content = content
        note.save()
        messages.success(request, "Note updated.")
    return redirect('dashboard')

@login_required
def delete_note(request, note_id):         
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect('dashboard')

@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user).order_by('subject_name')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('dashboard')
    else:
        form = SubjectForm()

    return render(request, 'notes/dashboard.html', {
        'subjects': subjects,
        'form': form
    })

@login_required
def subject_notepad(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.subject = subject                   
            note.save()
            return redirect('subject_notepad', subject_id=subject.id)
    else:
        form = NoteForm()

    notes = Note.objects.filter(user=request.user, subject=subject).order_by('-created_at')

    return render(request, 'notes/home.html', {
        'subject': subject,
        'notes': notes,
        'form': form,
    })

@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()

@login_required
def subject_images(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    images = SubjectImage.objects.filter(subject=subject).order_by('-uploaded_at')
    
    return render(request, 'notes/subject_images.html', {
        'subject': subject,
        'images': images
    })

@login_required
def upload_image(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        SubjectImage.objects.create(subject=subject, image=image_file)
        return redirect('subject_images', subject_id=subject.id)
    
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(SubjectImage, id=image_id, subject__user=request.user)

    if image.image:
        image.image.delete(save=False)
    
    image.delete()
    return redirect('subject_images', subject_id=image.subject.id)

@login_required
def download_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    subjects = Subject.objects.filter(user=request.user).order_by('subject_name')

    for subject in subjects:
        if y < 150:
            p.showPage()
            y = height - 50

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"{subject.subject_name}")
        y -= 25
        p.setFont("Helvetica", 12)
        p.drawString(50, y, f"College: {subject.college_name}")
        y -= 20
        p.drawString(50, y, f"Teacher: {subject.teacher_name}")
        y -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Notes:")
        y -= 20

        p.setFont("Helvetica", 11)
        notes = Note.objects.filter(user=request.user, subject=subject).order_by('-created_at')
        for note in notes:
            text = note.content[:400] + "..." if len(note.content) > 400 else note.content
            p.drawString(70, y, f"• {text}")
            y -= 18
            if y < 100:
                p.showPage()
                y = height - 50

        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Images:")
        y -= 25

        images = subject.images.all()
        for img in images:
            if y < 150:
                p.showPage()
                y = height - 50

            try:
                img_path = img.image.path
                img_reader = ImageReader(img_path)
                img_width = 200
                img_height = 150
                
                if img_width > 500:
                    ratio = 500 / img_width
                    img_width = 500
                    img_height = int(img_height * ratio)

                p.drawImage(img_reader, 50, y - img_height, width=img_width, height=img_height, preserveAspectRatio=True)
                y -= (img_height + 30)
                
            except:
                p.drawString(70, y, f"• Image could not be loaded: {img.image.name}")
                y -= 20
        y -= 40  

    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_notes.pdf"'
    return response