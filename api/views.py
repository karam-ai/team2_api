from django.shortcuts import render, HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("hello world")


def test(request):
    return HttpResponse(request.POST.items())
