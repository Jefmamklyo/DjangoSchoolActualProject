from django.forms import forms
from .models import Course
from functools import wraps
from django.core.exceptions import ValidationError

#define the decorator
def loggingDecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs): #define wrapper with args and kwargs
        #function which we are wrapping
        value = func(*args, **kwargs) #store function return values in a feild
        if value: #if value exists
            print("error exists") 
        return value
    return wrapper

class CourseValidator():
    def __init__(self, Name, Semester, Unit):
        self.Name = Name
        self.Semester = Semester
        self.Unit = Unit
    #________________
    #validation rules
    #________________

    def duplicate(self):
        #make coursename = form input
        if Course.objects.filter(name__iexact = self.Name).exists():
            return f"course '{self.Name}' exists"

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
            #store the return value
            error = i()
            #chcek if error exists
            if error:
                return error
            else:
                return []
    @loggingDecorator #decorate this function
    def Validate(self):
        #add validation function 
        Error = list(self.validationRun())
        if Error:
            raise ValidationError("This is an error")
        return []















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
    
