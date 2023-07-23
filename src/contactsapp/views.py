from datetime import date, timedelta
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Contact
from .forms import ContactForm


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('usersapp/index.html')
    else:
        form = ContactForm()
    return render(request, 'contactsapp/add_contact.html', context={'form': form})


@login_required
def update_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            return redirect('usersapp/index.html')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contactsapp/update_contact.html', context={'form': form, 'contact': contact})


@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('usersapp/index.html')
    return render(request, 'contactsapp/delete_contact.html', context={'contact': contact})


@login_required
def search_contact(request):
    search_query = request.GET.get('search_query', '')
    user_contacts = Contact.objects.filter(user=request.user)
    search_results = user_contacts.filter(
        models.Q(first_name__icontains=search_query) |
        models.Q(last_name__icontains=search_query) |
        models.Q(address__icontains=search_query) |
        models.Q(phone_number__icontains=search_query) |
        models.Q(email__icontains=search_query) |
        models.Q(birth_date__icontains=search_query)
    )

    context = {
        'search_query': search_query,
        'search_results': search_results
    }

    return render(request, 'contactapp/search_contacts.html', context)


@login_required
def upcoming_birthdays(request):
    if request.method == 'POST':
        days = request.POST.get('days', 0)
        days = int(days) if days else 0
        current_date = date.today()
        end_date = current_date + timedelta(days=days)
        result = []
        contacts = Contact.objects.filter(user=request.user)
        for contact in contacts:
            if contact.birth_date:
                birthday_date = date(year=date.today().year, month=contact.birth_date.month, day=contact.birth_date.day)
                birthday_date_next_year = date(year=date.today().year + 1, month=contact.birth_date.month,
                                               day=contact.birth_date.day)
                if date.today() < birthday_date <= end_date or date.today() < birthday_date_next_year <= end_date:
                    result.append(contact)

    else:
        result = []
    return render(request, 'contactsapp/upcoming_birthdays.html', context={'contacts': result})


@login_required
def detail_contact(request):
    contacts = Contact.objects.filter(user=request.user).order_by('first_name')
    return render(request, 'contactsapp/detail_contact.html', context={'contacts': contacts})
