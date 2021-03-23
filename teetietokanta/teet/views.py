from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Tea

import sqlite3

def index(request):
    teas = Tea.objects.all()
    context = {
        'teas': teas,
    }
    return render(request, 'teet/index.html', context)

def addNew(request):
    return render(request, 'teet/addnew.html')

def submitNew(request):
    name = request.POST['name']
    description = request.POST['description']

    if len(name) == 0 or len(description) == 0:
        return render(request, 'teet/addnew.html')

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    response = cursor.executescript("INSERT INTO teet_tea(name, description) VALUES('"+ name +"', '"+ description + "');")
    conn.commit()
		#Tea.objects.create(name=name, description=description)
    return HttpResponseRedirect(reverse('teet:index'))
