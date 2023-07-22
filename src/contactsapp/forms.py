from django.forms import ModelForm, CharField, TextInput, DateField, EmailField
from .models import Contact


class ContactForm(ModelForm):
    first_name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())
    last_name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())
    birth_date = DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'year-mount-day'}))
    phone_number = CharField(min_length=13, max_length=13, required=True, widget=TextInput())
    email = EmailField(required=True)
    address = CharField(min_length=4, max_length=50, required=True, widget=TextInput())
    sex = CharField()
    status = CharField()

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birth_date', 'phone_number', 'email',  'address', 'sex', 'status']