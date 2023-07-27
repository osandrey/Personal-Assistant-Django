from django.urls import path
from . import views


app_name = 'cloud_storageapp'

urlpatterns = [
    # path('authorize/', views.dropbox_oauth, name='dropbox_oauth'),
    # path('files/', views.all_files, name='all_files'),
    path('dropbox-folders/', views.dropbox_folders, name='dropbox_folders'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('success_upload/', views.success_upload, name='success_upload'),
    path('dropbox-folders/<path:folder_path>/', views.folder_files, name='folder_files'),
    path('download-file/<path:file_path>/', views.download_file, name='download_file'),

]