#other
from string.templatelib import Template
from django.http import HttpResponse
from django import shortcuts
from django.core.exceptions import ValidationError


#for class based views
from django.views.generic import CreateView, ListView, TemplateView

#import from Other Files
from .models import School, Course
from .forms import InputForms
from .service import CourseValidator
    
    
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

    


 
    
class View2(CreateView):
    model = Course
    form_class = InputForms
    template_name = "BSSSRemake/index.html"
    success_url = "/view2/"

    def form_valid(self, form):
        #access variables beofre submission
        Name = form.cleaned_data["name"]
        Semester = form.cleaned_data["semester1"]
        

        #initilise the CourseValidator and pass in parameters gotten from feild into the constructor
        validator = CourseValidator(Name, Semester)

        

        #run validate
        try:
            validator.Validate()
        except ValidationError as V:
            #add errors to form and redisplay
            form.add_error(None, V) #defines the error as general and not feild specficic
            return self.form_invalid(form)
            

        #save the form data to the database
        return super().form_valid(form)

     #get and populate variables in template, **kwargs allow vriable amount of kwargs to be passed through
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title view 2"
        context["content"] = "Comtent view 2"
        context["View2"] = True

        #Query school and courses while removing lazy loading
        context["courses"] = Course.objects.all()
        return context

    



