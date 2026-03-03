from django import shortcuts
from django.shortcuts import render, redirect

from django.http import HttpResponse

#http request parameter django autmatically passes to the view
def view1(request):
    #list
    return render(
        request,
        #Dictonariy of content in the template
        "BSSSRemake/index.html",
        {
            'title' : "View 1 title",
            'content' : "view 2 content"
            
           }
        
        )

def view2(request):
    #list
    return render(
        request,
        #Dictonariy of content in the template
        "BSSSRemake/index.html",
        {
            'title' : "View 2 title",
            'content' : "View 2 content"
            
           }
        
        )

# Create your views here.
