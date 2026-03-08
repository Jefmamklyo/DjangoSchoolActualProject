from django.http import HttpResponse

from django import shortcuts
#for class based views
from django.views.generic import TemplateView

from .models import School

    
    
    
class View1(TemplateView):
    template_name = "BSSSRemake/index.html"
    
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title view 1"
        context["content"] = "Content view 1"

        #Query school and courses while removing lazy loading
        context["schools"] = School.objects.prefetch_related("courses")
        return context
    


class View2(TemplateView):
    template_name = "BSSSRemake/index.html"

    #get and populate variables in template, **kwargs allow vriable amount of kwargs to be passed through
    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        context["title"] = "Title view 2"
        context["content"] = "Cpmtent view 2"
        return context
    




