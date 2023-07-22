from django.shortcuts import render
from .models import Contact


def view_forms_list(request):
    contact_model = Contact.objects.all()
    return render(request, 'contactsapp/list.html', {"contacts": contact_model})

