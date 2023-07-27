from django.urls import path
from . import views

app_name = 'notesapp'

urlpatterns = [
    path('add_tag/', views.add_tag, name="add_tag"),
    path('add_note/', views.add_note, name="add_note"),
    path('detail_note/<int:note_id>', views.detail_note, name="detail_note"),
    path('delete_note/<int:note_id>', views.delete_note, name="delete_note"),
    path('update_note/<int:note_id>', views.update_note, name="update_note"),
    path('search_note/', views.search_note, name="search_note"),
    path('tag_search/<int:tag_id>', views.tag_search, name="tag_search"),

]
