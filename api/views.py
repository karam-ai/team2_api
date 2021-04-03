from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *
from api.models import Drone
from rest_framework import routers, serializers, viewsets, permissions


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


import base64


@csrf_exempt
# POST DATA TO DB
def add_information(request):
    print("Qarsum super power: ", request.body)

    coded_string = request.POST['payload_raw']
    print("Mooza super powers: ", base64.b64decode(coded_string).decode('UTF-8'))
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


def get_information(request, pk):
    if request.method == 'GET':
        return JsonResponse({"measurements": None})


# Serializers define the API representation.
class DroneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drone
        fields = ['dev_id', 'hardware_serial', 'payload_row', 'meta_data']


# ViewSets define the view behavior.
class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'drones', DroneViewSet)


# Serializers define the API representation.
class MeasuresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'


# ViewSets define the view behavior.
class MeasuresViewSet(viewsets.ModelViewSet):
    queryset = Measures.objects.all()
    serializer_class = MeasuresSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'drones', DroneViewSet)
router.register(r'Measures', MeasuresViewSet)