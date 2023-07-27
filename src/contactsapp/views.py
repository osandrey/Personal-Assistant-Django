from datetime import date, timedelta
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from .models import Contact
from .forms import ContactForm, SendEmailForm
from personal_assistant.settings import RECIPIENTS_EMAIL, DEFAULT_FROM_EMAIL


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
    if search_query == ' ' or search_query == 'all':
        all_results = Contact.objects.all()
        return render(request, 'contactsapp/search_contact.html', {'all_results': all_results, 'search_query': search_query})
    else:
        context = {
            'search_query': search_query,
            'search_results': search_results
        }

        return render(request, 'contactsapp/search_contact.html', context)


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect(to='usersapp:success')
    else:
        form = ContactForm()
    return render(request, 'contactsapp/add_contact.html', context={'form': form})


@login_required
def update_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect(to="contactsapp:detail_contact", contact_id=contact_id)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contactsapp/update_contact.html',
                  context={'form': form, 'contact': contact})


@login_required
def detail_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    return render(request, 'contactsapp/detail_contact.html', context={'contact': contact})


@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect(to='usersapp:success')
    return render(request, 'contactsapp/delete_contact.html', context={'contact': contact})


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
    print(result)
    return render(request, 'contactsapp/upcoming_birthdays.html', context={'contacts': result})


@login_required
def send_email_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    contact_email = contact.email
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            print(subject)
            message = form.cleaned_data['message']
            print(message)
            from_email = contact_email
            print(from_email)
            try:
                send_mail(f'{subject} от {from_email}', message, DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect(to="contactsapp:detail_contact", contact_id=contact_id)
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'contactsapp/send_email_contact.html', {'form': SendEmailForm(request.POST), 'contact': contact})
