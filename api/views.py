from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("you used GET, please use POST")
