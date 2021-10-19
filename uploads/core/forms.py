from django import forms

from uploads.core.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

FILE_FORMAT_CHOICES = [("all", "All values"), 
    ("all_divide", "All values separated per IfcType"),
    ("unique", "Unique values"), 
    ("unique_divide", "Unique values separated per IfcType")]

class FileFormatForm(forms.Form):
    file_format = forms.ChoiceField(choices=FILE_FORMAT_CHOICES, widget=forms.RadioSelect())


