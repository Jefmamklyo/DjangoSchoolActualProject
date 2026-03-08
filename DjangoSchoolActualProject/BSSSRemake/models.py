from enum import unique
from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length = 50) #arbitrarty amount
    courses = models.ManyToManyField("Course") #Automatically craetes a junction table
    #Human readable values
    def __str__(self):
        return self.name

class Course(models.Model):
    achievementStandards = models.CharField(max_length = 50) #arbitrarty amount
    #Human readable values
    def __str__(self):
        return self.achievementStandards
