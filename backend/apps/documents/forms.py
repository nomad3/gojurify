from django import forms
from .models import DocumentTemplate
import json
from django.core.exceptions import ValidationError

class DocumentTemplateForm(forms.ModelForm):
    """
    Form for creating and editing document templates with enhanced validation
    and field handling.
    """
    
    # Add a hidden field for storing the JSON fields data
    fields_json = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'content', 'fields_json']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['fields_json'].initial = json.dumps(self.instance.fields)
            
    def clean_fields_json(self):
        """Validate and clean the fields JSON data."""
        try:
            fields_data = self.cleaned_data.get('fields_json')
            if not fields_data:
                return []
                
            fields = json.loads(fields_data)
            
            # Validate each field
            for field in fields:
                if 'name' not in field:
                    raise ValidationError("Each field must have a name.")
                if 'type' not in field:
                    raise ValidationError("Each field must have a type.")
                if field['type'] not in ['text', 'number', 'date', 'choice']:
                    raise ValidationError(f"Invalid field type: {field['type']}")
                    
            return fields
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format for fields.")
            
    def clean(self):
        """Perform cross-field validation."""
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        fields = cleaned_data.get('fields_json', [])
        
        # Validate that all field references in content exist in fields
        if content and fields:
            field_names = {field['name'] for field in fields}
            content_fields = set()
            import re
            # Find all field references in content (assuming format: {{field_name}})
            matches = re.findall(r'\{\{(\w+)\}\}', content)
            content_fields.update(matches)
            
            # Check for undefined fields
            undefined_fields = content_fields - field_names
            if undefined_fields:
                raise ValidationError(
                    f"Content references undefined fields: {', '.join(undefined_fields)}"
                )
                
        return cleaned_data
        
    def save(self, commit=True):
        """Save the form with proper field handling."""
        instance = super().save(commit=False)
        instance.fields = self.cleaned_data.get('fields_json', [])
        
        if commit:
            instance.save()
            
        return instance

