from django.forms import ModelForm, CharField, TextInput, Textarea, Form
from . import models


class TagForm(ModelForm):
    tag_name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(attrs={"class": "test_class"}))

    class Meta:
        model = models.Tag
        fields = ['tag_name']


class NoteForm(ModelForm):
    title = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=Textarea(attrs={"rows": "3"}))

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
