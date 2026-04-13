# documents/forms.py

from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "file", "conversion_type"]
        # conversion_type will automatically render as a dropdown
        # because we set choices= on the model field
