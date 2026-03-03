
#context processor creation
def customProc(request):
    #This fethces global data in this case being title and content from the template
    return{
        "projectName": 'BSSS Rework'
        }