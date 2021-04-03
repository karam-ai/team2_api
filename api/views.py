from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import *
from api.models import Drone
from rest_framework import routers, serializers, viewsets, permissions
import base64


# Create your views here.


@api_view(['POST'])
def addData(request):
    serializer = request.data
    print(serializer)
    key = serializer['payload_raw']
    print("payload_raw type:", type(key), ", value", key)
    payload = json.loads(base64.b64decode(key).decode('UTF-8'))
    print("payload: ", type(payload), payload)
    print('drone_id: ', get_drone_id_from_dev_id(serializer))
    measures = Measures.objects.create(drone_id=get_drone_id_from_dev_id(serializer), key='key', value=payload['key'])
    measures.save()
    return JsonResponse({'status': 200})


def get_drone_id_from_dev_id(serializer):
    try:
        drone = Drone.objects.get(dev_id=serializer['dev_id'])
        return drone.id
    except:
        new_drone = Drone.objects.create(dev_id=serializer['dev_id'], hardware_serial=serializer['hardware_serial'])
        new_drone.save()
        return new_drone.id


# Serializers define the API representation.
class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'


# ViewSets define the view behavior.
class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


# Serializers define the API representation.
class MeasuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'


# ViewSets define the view behavior.
class MeasuresViewSet(viewsets.ModelViewSet):
    queryset = Measures.objects.all()
    serializer_class = MeasuresSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Drones', DroneViewSet)
router.register(r'Measures', MeasuresViewSet)
