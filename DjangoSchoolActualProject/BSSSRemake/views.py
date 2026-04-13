#other
from string.templatelib import Template
from django.http import HttpResponse
from django import shortcuts
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

#for class based views
from django.views.generic import CreateView, ListView, TemplateView, View 

#import from Other Files
from .models import School, Course, ProjectInfo
from .forms import PROJECTFORMS, InputForms
from .service import CourseValidator
  
from .forms import InputForms, PROJECTFORMS

    
class View1(TemplateView):
    template_name = "BSSSRemake/index.html"
    
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title View 1"
        context["content"] = "Content View 1"
        context["schools"] = School.objects.prefetch_related("courses")
        context["View1"] = True
        return context

    


 
    
class View2(View):
    template_name = "BSSSRemake/index.html"

    def get(self, request):
        context = {
            "form": InputForms(),
            "projectForm": PROJECTFORMS(),
            "courses": Course.objects.all(),
            "ProjectInfo": ProjectInfo.objects.all(),
            "View2": True,
            "title": "Title view 2",
            "content": "Content view 2",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = InputForms(request.POST)
        projectForm = PROJECTFORMS(request.POST)

        # Identify which form was submitted
        if "course_submit" in request.POST:
            if form.is_valid():
                Name = form.cleaned_data["name"]
                Semester = form.cleaned_data["semester1"]

                validator = CourseValidator(Name, Semester)

                try:
                    validator.Validate()
                    form.save()
                    return redirect("/view2/")
                except ValidationError as V:
                    form.add_error(None, V)

        elif "project_submit" in request.POST:
            if projectForm.is_valid():
                projectForm.save()
                return redirect("/view2/")

        # If invalid, re-render with errors
        context = {
            "form": form,
            "projectForm": projectForm,
            "courses": Course.objects.all(),
            "ProjectInfo": ProjectInfo.objects.all(),
            "View2": True,
        }
        return render(request, self.template_name, context)
        
        
    



