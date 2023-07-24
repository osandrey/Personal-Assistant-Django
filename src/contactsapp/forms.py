from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'year-mount-day'}))
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    sex = forms.ChoiceField(required=True, choices=(("male", "male"), ("female", "female")))
    status = forms.ChoiceField(required=True, choices=(("family", "family"), ("friend", "friend"), ("partner", "partner"), ("colleague", "colleague"), ("other", "other")))

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birth_date', 'phone_number', 'email',  'address', 'sex', 'status']