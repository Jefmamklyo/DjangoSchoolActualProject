from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    semester1 = models.IntegerField(default=0, db_index = True)
    unitInformation = models.CharField(max_length=50, db_index=True, default="Unknown")

    

class School(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    courses = models.ManyToManyField(Course, blank=True)

class ProjectInfo(models.Model):
    projectChoices = [ #Sets choises
        ("RESEARCH","RESEARCH"),
        ("PROTOTYPE","PROTOTYPE"),      
        ("FINAL_BUILD","FINAL_BUILD"),
        ("REFLECTION","REFLECTION")
            ]
    courseChoices = [
        ("SOFTWARE","SOFTWARE"),
        ("PHYSICS","PHYSICS"),
        ("MATHS","MATHS"),
        ("ROBOTICS","ROBOTICS")

        ]
    project = models.CharField(
        max_length = 20,
        choices = projectChoices,
        )
    courseName = models.CharField(
        max_length = 20,
        choices = courseChoices,
        default = "SOFTWARE"
        )
    createdAt = models.DateTimeField(auto_now=True)