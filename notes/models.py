from django.db import models

class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content

    def get_length_info(self):
        import numpy as np
        text_array = np.array([len(self.content)])
        return f"Length: {text_array[0]} chars (numpy/OpenCV demo)"