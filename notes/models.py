from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes') 
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:40]}..."

    def get_length_info(self):
        import numpy as np
        text_array = np.array([len(self.content)])
        return f"Length: {text_array[0]} chars (numpy/OpenCV demo)"
    
class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    college_name = models.CharField(max_length=200)
    subject_name = models.CharField(max_length=150)
    teacher_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject_name} - {self.college_name}"
    
class SubjectImage(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='subject_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.subject.subject_name}"