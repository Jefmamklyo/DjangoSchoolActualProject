from .models import Course
from .models import ProjectInfo
from functools import wraps
from django.core.exceptions import ValidationError

from collections import defaultdict
from django.utils import timezone
from datetime import timedelta

import os

#define the decorator for loggig (DEBUG)
def loggingDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs): #define wrapper with args and kwargs
        #function which we are wrapping
         #store function return values in a feild
        try:
            value = func(*args, **kwargs)
            return value
        except ValidationError as e:
            print("Got an error", e)
            raise #raise the error again so the views cathces it
    return wrapper

class CourseValidator():
    def __init__(self, Name, Semester):
        self.Name = Name
        self.Semester = Semester
    #________________
    #validation rules
    #________________

    def duplicate(self):
        #make coursename = form input
        if Course.objects.filter(name__iexact = self.Name).exists():
            return f"Course '{self.Name}' exists"

    def semOutOfBounds(self):
        if self.Semester <= 0 or self.Semester > 4:
            return "Semester is out of bounds"


    #________________
    #validation rules activation
    #________________

    def validationRun(self):
        VRule = [
            self.semOutOfBounds,
            self.duplicate
            ]

        for i in VRule:
            #store the return value/ values
            error = i()
            #chcek if error exists
            if error:
                yield error
                

    @loggingDecorator #decorate this function
    def Validate(self):
        #add validation function 
        Error = list(self.validationRun())
        if Error:
            raise ValidationError(Error)
        return False



###________________________###
###_____Adjacecny list_____###
###________________________###

class conflictDetection():
    def __init__(self, queryset):

        self.queryset = queryset
        self.graph = defaultdict(lambda: defaultdict(int))

    def timeWeight(self, obj):
        now = timezone.now()
        timeChange = now - obj.createdAt

        seconds = timeChange.total_seconds()

        weighting = (seconds * 0.99)  + 1

        return weighting
        
    
    def createAdjacency(self):
        
        #create adjacecy
        for obj in self.queryset:
            courseName = obj.courseName
            projectName = obj.project
            weight = self.timeWeight(obj)

            self.graph[courseName][projectName] += weight
     
    def normolizeList(self):
        #list to store normlolised list
        listNormalized = {}

        #courses is key 1, project is key 2
        for course, project in self.graph.items():
            total = sum(project.values())
            

            if total > 0:  #avoid 0 divis   ion 
                #dictionary compherehension
                listNormalized[course] = { 
                    k : v/ total 
                    for k, v in project.items()       
                    }
               
            #repeat loop if there is a 0 division
          
        return listNormalized

    def reccomendation(self, graph, choiceAmount = 2):
        #reccomed with alogirthms to before passing to views
            #create an algorithm whuich gets the greatest values form the reverse adjanecy list graphs 
        sortedDict = {}

        for courses, projects in graph.items():
            sortedProjects = sorted(
                projects.items(),
                key = lambda x: x[1],
                reverse = True           
                )
            sortedDict[courses] = sortedProjects[:choiceAmount]
        return sortedDict
        
    
    def run(self):
        self.createAdjacency()
        normalised = self.normolizeList()
        return self.reccomendation(normalised)

    def runMax(self):
        self.createAdjacency()
        normalised = self.normolizeList()

        #loop thourgh frist key

        bCourse, bProject, topWeight = max(
                ( 
                    (course, project, weight) 
                    for course, projects in normalised.items() 
                    for project, weight in  projects.items()
                ),
                key = lambda x: x[2],
                default = (None,None, 0)
            )             
        return bCourse, bProject


###________________________###
###_____File Valdation_____###
###________________________###

###Decorators 

import magic 

allowedMimeTypes = ['img/png', 'img.jpeg', 'application/pdf']
def mimeCheckDecorator(func):
    @wraps(func)
    def wrapper(file, *args, **kwargs):
        mime = magic.from_buffer(file.read(1024), mime = True) #read the first 1024 bitest o get mime type
        file.seek(0) #reset buffer

        if mime not in allowedMimeTypes:
            return f"Not allows file type {mime}"
        return func(file, *args, **kwargs)
    return wrapper


def fileSizeCheckDecorator(maxFileSize):
    def decorator(func):
        @wraps(func)
        def wrapper(file, *args, **kwargs):
            if file.size > maxFileSize * 1024 * 1024: #coverts to megabytes
                return f"{file.name} bigger than {maxFileSize}"
            return func(file, *args, **kwargs)
        return wrapper
    return decorator

def sanitizeFileNameDecorator(func):
    @wraps(func)
    def wrapper(file, *args, **kwargs):
        cleaned = "".join(c for c in file if c.isalnum() or c in (' ', '.', '_')).rstrip()
        file = cleaned
        return func(file, *args, **kwargs)
    return wrapper

##saving
import uuid

def uniqueFileName(name):
    return f"{uuid.uuid4().hex}_{name}"


uploadDIR = os.path.join(settings.MEDIA_ROOT, "uploads")

@fileSizeCheckDecorator(5) #5mb 
@mimeCheckDecorator()
@sanitizeFileNameDecorator
def saveFile(file):

    #dynamically creating upload dir
    if not os.path.exists(uploadDIR):
        os.makedirs(uploadDIR)

    #Creating unique filenaem
    filename = uniqueFileName(file.name)
    path = os.path.join(uploadDIR)
    #saving
    with open(path, "wb+")  as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return filename



        



















# class ConflictService():

#     def buildAdjacencyList():

#             allCourse = Course.objects.all()
#             ID = [course.pk for course in allCourse]  #list comphrehsnion
#             Semesters = [course.semester1 for course in allCourse] #list comphrehsnion

#             #Dict comphrehension to zip them together
#             IdNames = {k:v for (k,v) in zip(ID, Semesters)}

#             #group by semseers
#             semsterGroup= defaultdict(list)

#             for course in allCourse:
#                 semesterGroup = [course.semester1].append(course.pk)

            
#             adjacency = defaultdict(list)
        
#             for semester, courseID in semesterGroup.items(): #for primarykey, value in semstergroup
#                 for currentCourse in courseID:
#                     #add all courses in the semester as conflicts
#                     conflicts = [
#                         c for c in courseID if c != currentCourse
#                     ]
#                     adjacency[currentCourse].append(conflicts)
                    

#             return dict(adjacency)
#
#