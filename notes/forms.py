from django import forms
from .models import Note, SubjectImage

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your text...'}),
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = SubjectImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'accept': 'image/png, image/jpeg, image/jpg'
            })
        }

from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['college_name', 'subject_name', 'teacher_name']
        widgets = {
            'college_name': forms.TextInput(attrs={'placeholder': 'College Name', 'style': 'width:300px'}),
            'subject_name': forms.TextInput(attrs={'placeholder': 'Subject Name', 'style': 'width:300px'}),
            'teacher_name': forms.TextInput(attrs={'placeholder': 'Teacher Name', 'style': 'width:300px'}),
        }