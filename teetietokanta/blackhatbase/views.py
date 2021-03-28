from django.shortcuts import render

# Create your views here.

from .models import Content
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import json

def index(request):
    content = Content.objects.all()
    context = {
        'content': content,
    }
    return render(request, 'blackhatbase/index.html', context)

@csrf_exempt
def submitNew(request):
		content = request.GET.get('cookie')
		Content.objects.create(content=content)
		return HttpResponseRedirect(reverse('blackhatbase:index'))
