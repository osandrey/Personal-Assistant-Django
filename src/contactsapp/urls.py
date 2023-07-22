
from .views import view_forms_list
from django.urls import path



app_name = 'contactsapp'

urlpatterns = [
    path('', view_forms_list, name='view_forms_list'),
    ]