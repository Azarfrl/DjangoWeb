from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes') 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:40]}..."

    def get_length_info(self):
        import numpy as np
        text_array = np.array([len(self.content)])
        return f"Length: {text_array[0]} chars (numpy/OpenCV demo)"