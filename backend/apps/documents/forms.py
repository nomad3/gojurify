from django import forms
from .models import DocumentTemplate

class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'content', 'fields']
        widgets = {
            'fields': forms.HiddenInput(),
        }
