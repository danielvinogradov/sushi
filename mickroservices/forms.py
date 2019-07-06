from django import forms
from django.core.validators import EmailValidator

from .models import QuestionModel

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        exclude = ['name','status',]
        widgets = {
            'body': forms.Textarea(attrs={'rows':5}),
        }