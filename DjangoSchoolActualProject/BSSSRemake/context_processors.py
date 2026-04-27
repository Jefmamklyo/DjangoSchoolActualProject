
#context processor creation
def customProc(request):
    #This fethces global data in this case being title and content from the template
    return{
        "projectName": 'BSSS Rework',
        "LView1": "View1",
        "LView2": "View2",
        "LReccomendation": "Reccomendation"
        }