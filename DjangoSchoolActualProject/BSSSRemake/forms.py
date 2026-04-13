from django import forms
from django.forms import fields
from .models import Course, ProjectInfo

class InputForms(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
class PROJECTFORMS(forms.ModelForm):
    class Meta:
        model = ProjectInfo
        fields = "__all__"