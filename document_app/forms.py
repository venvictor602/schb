from django import forms
from .models import DocumentData

class DocumentForm(forms.ModelForm):
    pdf_file1 = forms.FileField(required=False, label="PDF File 1")  # First PDF upload field
    pdf_file2 = forms.FileField(required=False, label="PDF File 2")  # Second PDF upload field
    
    class Meta:
        model = DocumentData
        fields = '__all__'  # Include all fields from DocumentData

      
