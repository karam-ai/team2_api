from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return HttpResponse("hello world")

@csrf_exempt
def test(request):
    return HttpResponse("posted data: \n" + request.POST.items())
