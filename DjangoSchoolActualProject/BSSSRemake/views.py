from django.shortcuts import render

from django.http import HttpResponse

#http request parameter django autmatically passes to the view
def index(request):
    return render(
        request,
        "BSSSRemake/index.html",
        {
            'content': "This is a test"
            
           }
        
        )



# Create your views here.
