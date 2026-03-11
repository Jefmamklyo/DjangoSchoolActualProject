from .models import Course
from collections import defaultdict





class ConflictService():

    def buildAdjacencyList():

            allCourse = Course.objects.all()
            ID = [course.pk for course in allCourse]  #list comphrehsnion
            Semesters = [course.semester1 for course in allCourse] #list comphrehsnion

            #Dict comphrehension to zip them together
            IdNames = {k:v for (k,v) in zip(ID, Semesters)}

            #group by semseers
            semsterGroup= defaultdict(list)

            for course in allCourse:
                semesterGroup = [course.semester1].append(course.pk)

            
            adjacency = defaultdict(list)
        
            for semester, courseID in semesterGroup.items(): #for primarykey, value in semstergroup
                for currentCourse in courseID:
                    #add all courses in the semester as conflicts
                    conflicts = [
                        c for c in courseID if c != currentCourse
                    ]
                    adjacency[currentCourse].append(conflicts)
                    

            return dict(adjacency)
    
