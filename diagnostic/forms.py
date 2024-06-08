from django import forms
from .models import Diagnostic

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = '__all__'
