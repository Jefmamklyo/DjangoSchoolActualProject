from django.contrib import admin
from .models import School, Course

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "display_courses")
    filter_horizontal = ("courses",)  # nicer UI for selecting/deselecting courses

    def display_courses(self, obj):
        return ", ".join(course.name for course in obj.courses.all())
    display_courses.short_description = "Courses"

# Register your models here.
admin.site.register(School)
admin.site.register(Course)

