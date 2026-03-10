from string.templatelib import Template
from django.db.models import F
from django.forms import Form, fields
from django.http import HttpResponse

from django import shortcuts
#for class based views
from django.views.generic import CreateView, ListView, TemplateView

from .models import School, Course


from .forms import InputForms
from django.views.generic.edit import FormView
    
    
class View1(TemplateView):
    template_name = "BSSSRemake/index.html"
    
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title View 1"
        context["content"] = "Content View 1"

        
        return context
    


 
    
class View2(CreateView):
    model = Course
    form_class = InputForms
    template_name = "BSSSRemake/index.html"
    success_url = "/view2/"

     #get and populate variables in template, **kwargs allow vriable amount of kwargs to be passed through
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title view 2"
        context["content"] = "Comtent view 2"
        context["View2"] = True

        #Query school and courses while removing lazy loading
        context["courses"] = Course.objects.select_related()
        return context

    



