from django import forms
from django.template.defaultfilters import slugify

from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text', 'public']
        #labels = {'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
    
    def clean(self):
        cleaned_data = super().clean()
        slug = slugify(cleaned_data.get('title'))
        if 'title' in self.changed_data:
            try:
                Entry.objects.get(slug=slug)
            except Entry.DoesNotExist:
                cleaned_data['slug'] = slug
                return cleaned_data
            else:
                self.add_error('title', 'This title is already in use.')