from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, db_index = True)  # Name of the course , Indexed

    #Human readable values
    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields = ["name"], name = "courseIndex")
            ]
 


#defined course after
class School(models.Model):
    name = models.CharField(max_length=50, db_index = True)  # Name of the school, Indexed
    courses = models.ManyToManyField(Course, blank=True)  # Many to Many link

    #Human readable values
    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields = ["name"], name = "schoolIndex")
            ]