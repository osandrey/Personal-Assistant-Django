from datetime import date, timedelta
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse
from .models import Contact

from .forms import SendEmailForm, ContactForm
from .models import Contact
from dotenv import dotenv_values
import os
import smtplib
import ssl
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

CONFIG = dotenv_values('.env')
MetaLogin = CONFIG.get("EMAIL_HOST_USER")
MetaPassword = CONFIG.get("EMAIL_HOST_PASSWORD")


@login_required
def search_contact(request):
    search_query_contact = request.GET.get('search_query', '')
    user_contacts = Contact.objects.filter(user=request.user)
    search_results_contact = user_contacts.filter(
        models.Q(first_name__icontains=search_query_contact) |
        models.Q(last_name__icontains=search_query_contact) |
        models.Q(address__icontains=search_query_contact) |
        models.Q(phone_number__icontains=search_query_contact) |
        models.Q(email__icontains=search_query_contact) |
        models.Q(birth_date__icontains=search_query_contact)
    )
    if search_query_contact == ' ' or search_query_contact == 'all':
        all_results_contact = Contact.objects.all()
        context = {
            'all_results_contact': all_results_contact,
            'search_query_contact': search_query_contact
        }
        return render(request, 'contactsapp/search_contact.html', context)
    else:
        context = {
            'search_query_contact': search_query_contact,
            'search_results_contact': search_results_contact
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
def send_email(self, request, obj):
    if request.method == 'POST':
        print('I am in send email POST method!')
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # File upload handling logic

            attachment_file: InMemoryUploadedFile = form.cleaned_data['attachment']
            file_path = self.handle_uploaded_file(attachment_file)
            # Process the file as needed
            print('I am in sending email form is OK!')
            print(form.cleaned_data)

            run_send_email(obj, form.cleaned_data, file_path)
            return render(request, 'usersapp/success.html')
    else:
        form = SendEmailForm()
    return render(request, 'contactsapp/send_email.html', {'form': form})


class ContactObjectMixin(object):
    model = Contact

    def get_object(self):
        _id = self.kwargs.get('id')
        obj = None
        if _id is not None:
            obj = get_object_or_404(self.model, pk=_id)
        return obj

    def get_id(self):
        return self.kwargs.get("id")


class ContactSendEmail(ContactObjectMixin, View):
    template_name = 'contactsapp/send_email.html'  # DetailView

    def get(self, request, _id=None, *args, **kwargs):
        # GET method
        print('I am get method')
        context = {}
        obj = self.get_object()
        form = SendEmailForm()
        if obj is not None:
            context['object'] = obj

        return render(request, self.template_name, context={"form": form, "object": obj})

    def post(self, request, id=None, *args, **kwargs):
        # POST method
        print('I am post method')
        context = {}
        obj = self.get_object()
        if obj is not None:
            self.send_email(request, obj)
            context['object'] = None
            return redirect('/contactsapp/')
        return render(request, self.template_name, context)

    def handle_uploaded_file(self, file: InMemoryUploadedFile):
        # Generate a unique file name
        file_name = file.name
        upload_folder_path = "uploads/"
        if not os.path.exists(upload_folder_path):
            os.mkdir(upload_folder_path)

        file_path = upload_folder_path + file_name

        # Read the file contents
        file_contents = file.read()

        # Save the file to disk
        with open(file_path, 'wb') as destination:
            destination.write(file_contents)
        return file_path

    def send_email(self, request, obj):
        if request.method == 'POST':
            print('I am in send email POST method!')
            form = SendEmailForm(request.POST, request.FILES)
            if form.is_valid():
                # File upload handling logic

                attachment_file: InMemoryUploadedFile = form.cleaned_data['attachment']
                file_path = self.handle_uploaded_file(attachment_file)
                # Process the file as needed
                print('I am in sending email form is OK!')
                print(form.cleaned_data)

                run_send_email(obj, form.cleaned_data, file_path)
                return render(request, 'usersapp/success.html')
        else:
            form = SendEmailForm()
        return render(request, 'contactsapp/send_email.html', {'form': form})


def run_send_email(obj: Contact, data: dict, file_path: str):
    user_name = obj.first_name + " " + obj.last_name
    print(user_name)
    Sender = MetaLogin
    Sender_password = MetaPassword
    receiver_email = obj.email
    print(receiver_email)
    subject = f"Subject: Greetings, dear {user_name}, {data['theme']}"
    message = data['text']
    attachment_name = os.path.basename(file_path)
    with open(file_path, 'rb') as attachment:
        mail = EmailMessage(subject=subject, body=message, from_email=Sender, to=[receiver_email],
                            cc=[data.get('coppy_to')])
        mail.attach(attachment_name, attachment.read(), data.get('attachment').content_type)
        mail.send()
