from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'year-mount-day'}))
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    sex = forms.CharField()
    status = forms.CharField()

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birth_date', 'phone_number', 'email',  'address', 'sex', 'status']