from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *


# Create your views here.

def index(request):
    return HttpResponse("hello world")


@csrf_exempt
def test(request):
    if request.POST:
        data = request.body
        data = '{"' + data.decode('utf-8').replace('=', '":"') + '"}'
        data = data.replace('&', '","')
        print(type(data), data)
        data = json.loads(data)
        print(data)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse("you used GET, please use POST")


@csrf_exempt
# POST DATA TO DB
def add_information(request):
    if request.method == 'POST':
        try:

            info = Information.objects.create(drone_name=request.POST['drone_name'],
                                              drone_number=request.POST['drone_number'],
                                              long=request.POST['long'],
                                              lat=request.POST['lat'])
            info.save()
            return JsonResponse({'status': '200'})
        except Exception as e:
            return HttpResponse("something is wrong with it" + str(e))
    else:
        return HttpResponse("you used GET, please use POST")
