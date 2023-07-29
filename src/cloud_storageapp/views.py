import os
from pathlib import Path

import requests
from django.http import JsonResponse, FileResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
import environ
import dropbox
from .forms import FileUploadForm


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")
# print(f'{BASE_DIR} ~~ YOUR BASE_DIR')

# /Users/ekaterina/Documents/GitHub/Personal-Assistant-Django
Secret_Key = env("SECRET_KEY")
# Create your views here.

DROPBOX_APP_KEY = env("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = env("DROPBOX_APP_SECRET")
DROPBOX_OAUTH2_REFRESH_TOKEN = env("DROPBOX_OAUTH2_REFRESH_TOKEN")


# def dropbox_oauth(request):
#     return redirect(f'https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri=http://127.0.0.1:8000/cloud_storageapp/authorize/&response_type=code')
#
#
# def all_files(request):
#     data = requests.post('https://api.dropboxapi.com/2/files/search_v2', headers={
#         'Authorization': f'Bearer {DROPBOX_OAUTH2_REFRESH_TOKEN}'}, json={
#         "query": "class"
#     })
#     return JsonResponse(data.json())

def dropbox_folders(request):
    # Replace 'YOUR_DROPBOX_ACCESS_TOKEN' with your Dropbox access token
    access_token = DROPBOX_OAUTH2_REFRESH_TOKEN
    dbx = dropbox.Dropbox(access_token)

    # List all files in the root directory
    folders = []
    for entry in dbx.files_list_folder('', recursive=True).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            folders.append(entry)

    context = {'folders': folders}
    return render(request, 'dropbox_folders.html', context)



def folder_files(request, folder_path):
    print(str(folder_path).strip('/'))
    access_token = DROPBOX_OAUTH2_REFRESH_TOKEN
    dbx = dropbox.Dropbox(access_token)
    # folder_path = str(folder_path).strip('/')
    # List all files in the specified folder
    files = []
    try:
        result = dbx.files_list_folder(folder_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                files.append(entry)
    except dropbox.exceptions.ApiError as e:
        if e.error.is_path() and \
                e.user_message_text.startswith("not_folder/"):
            # The provided path is not a folder path, handle the error as needed
            pass
        else:
            raise

    context = {'files': files, 'folder_path': folder_path}
    return render(request, 'folder_files.html', context)



    # for entry in dbx.files_list_folder(folder_path).entries:
    #     if isinstance(entry, dropbox.files.FileMetadata):
    #         files.append(entry)
    #
    # context = {'files': files, 'folder_path': folder_path}
    # return render(request, 'folder_files.html', context)



def success_upload(request):
    return render(request, 'upload_success.html', {})



def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Replace 'YOUR_DROPBOX_ACCESS_TOKEN' with your Dropbox access token
            access_token = DROPBOX_OAUTH2_REFRESH_TOKEN
            dbx = dropbox.Dropbox(access_token)
            folder = form.cleaned_data['folder']

            file = request.FILES['file']
            file_path = f'/{folder}/{file.name}' if folder else f'/{file.name}'

            dbx.files_upload(file.read(), file_path)

            # Redirect to a success page or display a success message
            return redirect(to='cloud_storageapp:success_upload')

    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})



def download_file(request, file_path):

    file_full_path = 'cloud_storageapp/download-file/'+file_path
    print(f'FILE PASSSSSSSSSS    {file_full_path}')
    access_token = DROPBOX_OAUTH2_REFRESH_TOKEN
    dbx = dropbox.Dropbox(access_token)
    # file = request.FILES['file']
    try:
        metadata, response = dbx.files_download(file_full_path)

    except dropbox.exceptions.ApiError as e:
        return HttpResponseNotFound("File not found. Exeption from except!")

    file_content = response.content
    content_type = metadata.mime_type
    response = FileResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_full_path)}"'
    return redirect(to='cloud_storageapp:folder_files')









    # Check if the file exists
    # if os.path.exists(file_full_path):
    #     # Open the file in binary mode and create a FileResponse to stream the file to the client
    #     with open(file_full_path, 'rb') as file:
    #         response = FileResponse(file, content_type='application/octet-stream')
    #         # Set the content disposition header to force the file download
    #         response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_full_path)}"'
    #         return response
    # else:
    #     # Return a 404 Not Found response if the file does not exist
    #     return HttpResponseNotFound("File not found.")