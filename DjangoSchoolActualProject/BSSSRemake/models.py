from enum import unique
from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length = 50) #arbitrarty amount
    #Human readable values
    def __str__(self):
        return self.name

class Course(models.Model):
    achievementStandards = models.CharField(max_length = 50) #arbitrarty amount
    #Human readable values
    def __str__(self):
        return self.achievementStandards

#Junction Table
class schoolCourses(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
        #constraints to prevent duplicates
    class Meta:
        unique_together = ("school", "course")