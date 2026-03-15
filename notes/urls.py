from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_note, name='add_note'),  
    path('note/<int:note_id>/update/', views.update_note, name='update_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]