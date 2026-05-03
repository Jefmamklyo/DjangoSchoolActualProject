#other
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import os 
from django.conf import settings
from django.contrib import messages


#for class based views
from django.views.generic import CreateView, ListView, TemplateView, View, FormView

#import from Other Files
from .models import School, Course, ProjectInfo
from .forms import InputForms, PROJECTFORMS, UploadFile
from .service import CourseValidator
from .service import conflictDetection
from . service import saveFile
    
    
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

      

   
############################################################
#______________________Adjacecny List______________________#
############################################################
class Reccomendation(CreateView):
    template_name = "BSSSRemake/index.html"
    success_url = "/recommendation/"
    form_class = PROJECTFORMS
    model = ProjectInfo

    def get_initial(self):
        initial = super().get_initial()

        data = ProjectInfo.objects.all()
        cd = conflictDetection(data)
    
        course, project = cd.runMax()
        
        initial["courseName"] = course
        initial["project"] = project

        return initial

    def get_context_data(self, **kwargs):
        #calls the parent method to get context
        context = super().get_context_data(**kwargs)
        
        # Query project fields
        projInf = ProjectInfo.objects.all()
        context["ProjectInfo"] = projInf
        context["projectForm"] = context["form"]  
        context["Reccomendation"] = True

        #run reccomendation
        cd = conflictDetection(projInf)
        context["recommendations"] = cd.run()

        
        return context
############################################################
#_______________________File Uploads_______________________#
############################################################
class UploadFiles(FormView):
    template_name = "BSSSRemake/index.html"
    form_class = UploadFile
    success_url = "/upload/"#add somethign here 

    def getFiles(self):
        path = os.path.join(settings.MEDIA_ROOT, "uploads")

        #null chaining
        if not os.path.exists(path):
            return []

        return os.listdir(path)

    def form_valid(self, form):
        uploadedFiles = self.request.FILES.getlist("files")
        for file in uploadedFiles:
           try:
                errors = []
                filename = saveFile(file,errors)
                messages.success(self.request, f"{filename} was uploaded")
           except ValidationError as e:
               for error in e.messages:
                   messages.error(self.request, f"{file.name}: {error}")

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formUpload"] = UploadFile()
        context["uploadForm"] = True
        context["files"] = self.getFiles()
        return context