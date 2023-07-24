from django.forms import ModelForm, CharField, TextInput, Textarea, Form
from . import models


class TagForm(ModelForm):
    name = CharField(required=True)

    class Meta:
        model = models.Tag
        fields = ['name']


class NoteForm(ModelForm):
    title = CharField(required=True)
    description = CharField(required=True)

    class Meta:
        model = models.Note
        fields = ['title', 'description']
        exclude = ['tags']


class NoteSearchForm(Form):
    keyword = CharField(max_length=100, required=False, widget=TextInput(attrs={'placeholder': 'Search'}))

    def search(self, queryset):
        keyword = self.cleaned_data.get('keyword')
        if keyword:
            queryset = queryset.filter(title__icontains=keyword) | queryset.filter(description__icontains=keyword)
        return queryset
