from django.shortcuts import render

def index(request):
    return render(request, 'teet/index.html')

def addNew(request):
    return render(request, 'teet/addnew.html')
