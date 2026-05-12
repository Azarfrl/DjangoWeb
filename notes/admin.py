from django.contrib import admin
from .models import Note, Subject, SubjectImage

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_short', 'created_at', 'user')
    search_fields = ('content',)
    readonly_fields = ('created_at',)

    def content_short(self, obj):
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content
    content_short.short_description = "Content"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'college_name', 'teacher_name', 'user')
    search_fields = ('subject_name', 'college_name')
    list_filter = ('user',)

# ← NEW: Register SubjectImage
@admin.register(SubjectImage)
class SubjectImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'uploaded_at')
    list_filter = ('subject', 'uploaded_at')
    search_fields = ('subject__subject_name',)