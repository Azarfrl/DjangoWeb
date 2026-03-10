from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content_short', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)

    def content_short(self, obj):
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content
    content_short.short_description = "Content"