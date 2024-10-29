from django import forms
from .models import DocumentTemplate

class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'content', 'fields', 'owners', 'version']
        widgets = {
            'fields': forms.HiddenInput(),
            'owners': forms.SelectMultiple(),
            'version': forms.NumberInput(),
        }

