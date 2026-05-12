from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),       
    path('subject/<int:subject_id>/notepad/', views.subject_notepad, name='subject_notepad'),
    path('subject/<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
    path('add/<int:subject_id>/', views.add_note, name='add_note'),
    path('add/', views.add_note, name='add_note'),
    path('note/<int:note_id>/update/', views.update_note, name='update_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('subject/<int:subject_id>/images/', views.subject_images, name='subject_images'),
    path('subject/<int:subject_id>/upload-image/', views.upload_image, name='upload_image'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]