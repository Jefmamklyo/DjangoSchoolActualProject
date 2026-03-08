from django.db import models

# Create your models here.




class Course(models.Model):
    name = models.CharField(max_length=50)  # Name of the course
    #Human readable values
    def __str__(self):
        return self.name


#defined course after
class School(models.Model):
    name = models.CharField(max_length=50)  # Name of the school
    courses = models.ManyToManyField(Course, blank=True)  # link to courses
    #Human readable values
    def __str__(self):
        return self.name