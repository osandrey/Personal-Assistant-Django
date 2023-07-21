from django.urls import path
from . import views

app_name = "notesapp"

urlpatterns = [
    # path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('add_tag/', views.add_tag, name="add_tag"),
    path('add_note/', views.add_note, name="add_note"),
    path('detail/<int:note_id>', views.detail, name="detail"),
    path('delete_note/<int:note_id>', views.delete_note, name="delete_note"),
    path('update_note/<int:note_id>', views.update_note, name="update_note"),

]
