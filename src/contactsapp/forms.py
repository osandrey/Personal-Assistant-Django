from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'year-mount-day'}))
    sex = forms.ChoiceField(required=True, choices=(("male", "male"), ("female", "female")))
    status = forms.ChoiceField(required=True, choices=(("family", "family"), ("friend", "friend"), ("partner", "partner"), ("colleague", "colleague"), ("other", "other")))

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email',  'address',  'birth_date', 'sex', 'status']


class SendEmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = ['subject', 'message']