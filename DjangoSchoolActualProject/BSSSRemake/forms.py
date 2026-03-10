from django import forms
from django.forms import fields
from .models import Course

class InputForms(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name","semester1", "unitInformation"]
