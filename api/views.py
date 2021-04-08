from datetime import datetime

from django.core.checks import register
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
import binascii
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
    # base64 decode
    payload_str = base64.b64decode(key).decode('UTF-8')
    print("payload_to_base64", str(payload_str))
    # ascii decode
    ascii = [ord(c) for c in payload_str]
    # binary = bin(int(binascii.hexlify(payload_str), 16))
    print("payload_to_ascii", ascii, ', Length: ', len(ascii))
    measurements_from_ttn = conversion(ascii)
    print("measurements: ", measurements_from_ttn)

    new_measurements = Measurements.objects.create(lat=measurements_from_ttn['location']['lat'],
                                                   long=measurements_from_ttn['location']['long'],
                                                   data_type=measurements_from_ttn['data']['type'],
                                                   data_results=measurements_from_ttn['data']['results'],
                                                   droneId=measurements_from_ttn['droneId'],
                                                   date_entry=measurements_from_ttn['date_entry']
                                                   )

    new_measurements.save()

    # payload_str_test = str({"key": "1999"}).replace("'", '"')

    # payload_str = str(payload_str).replace("'", '"').replace("\n", "").replace(" ", "")

    # print("payload_str_test:", payload_str_test)

    print("payload_str:", payload_str)
    chrs = []
    for i in payload_str:
        chrs.append(i)

    for i in chrs:
        print(i, payload_str.count(i))

    # print("are they the same?:", len(payload_str), len(payload_str_test))
    #
    # payload = json.loads(payload_str)
    # print("payload: ", type(payload), payload)
    # print('drone_id: ', get_drone_id_from_dev_id(serializer))
    # measures = Measures.objects.create(drone_id=get_drone_id_from_dev_id(serializer), key='key', value=payload['key'])
    # measures.save()
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
class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = '__all__'


# ViewSets define the view behavior.
class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurements.objects.all()
    serializer_class = MeasurementsSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Drones', DroneViewSet)
router.register(r'Measurements', MeasurementsViewSet)


def makeObjectDate(array):
    print("makeObjectDate:", array)
    date = array[0]
    month = array[1] - 1
    year = 20 + array[2]
    hour = array[3]
    minute = array[4]
    date_entry = str(date) + "/" + str(month) + "/" + str(year) + "|" + str(hour) + ":" + str(minute)

    date1 = datetime(year, month, date, hour, minute, 0)

    return {"date_entry": date1}


def makeObjectDroneId(array):
    print("makeObjectDroneId:", array)
    id = array[0]
    return {'droneId': id}


def getArray(array, start_index, max):
    print("getArray:", array)

    new_array = []
    index = 0
    while (index < max):
        new_array.append(array[start_index + index])
        index += 1

    return new_array


def addingBytes(array):
    print("addingBytes:", array)
    new1 = (array[3] << 24) | (array[2] << 16) | (array[1] << 8) | array[0]
    return new1


def makeObjectLocation(array):
    print("makeObjectLocation: ", array)
    lat = addingBytes(getArray(array, 0, 4)) / 100000
    long = addingBytes(getArray(array, 4, 4)) / 100000

    return {"location": {"lat": lat, "long": long}}


def makeObjectData(array):
    print("makeObjectData: ", array)
    type = array[0]
    results = addingBytes(getArray(array, 1, 4))
    return {"data": {"type": type, "results": results}}


# team2 encoding
def conversion(array):
    measurements = {}

    for index in range(len(array)):
        if array[index] == 82:
            new_array = getArray(array, index + 1, 8)
            measurements.update(makeObjectLocation(new_array))
            print(measurements)
            index += 8
        if array[index] == 85:
            new_array = getArray(array, index + 1, 5)
            measurements.update(makeObjectDate(new_array))
            print(measurements)
            index += 5
        if array[index] == 83:
            new_array = getArray(array, index + 1, 1)
            measurements.update(makeObjectDroneId(new_array))
            print(measurements)

            index += 1
        if array[index] == 84:
            new_array = getArray(array, index + 1, 5)
            measurements.update(makeObjectData(new_array))
            print(measurements)

            index += 5

    return measurements
