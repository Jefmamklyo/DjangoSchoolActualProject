from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    semester1 = models.IntegerField(default=0, db_index = True)
    unitInformation = models.CharField(max_length=50, db_index=True, default="Unknown")

    

class School(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    courses = models.ManyToManyField(Course, blank=True)
