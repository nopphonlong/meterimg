from meterimg.models import Meter, Images
from meterimg.serializers import ImageSerializers, JustimageimageSerializers
from rest_framework import permissions, viewsets, mixins, status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gauge_reader_main.models.Gauge_classification import getpredict
from gauge_reader_main.models.guage_reading import get_gauge_value
import json
from django.http import HttpResponse


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj


class ImageViewset(viewsets.ModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = ImageSerializers


class JustImageViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = JustimageimageSerializers


@api_view(['GET', 'POST', 'DELETE'])
def test(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        img = Meter.objects.all()
        serializer = ImageSerializers(img, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ImageSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            img_path = serializer.data['meter_main_img'][1:]
            print(img_path)
            gauge_types = getpredict(img_path)
            gauge_value = get_gauge_value(img_path, min_value=-1, max_value=3, scale_width=0.5, scale_height=0.5)
            # print(value)
            print(f"Predicted Class: {gauge_types[0]}, {gauge_types[1]:0.2f}%\n")
            print(f"Gauge reading value: {gauge_value} bar ")
            gauge_dict = {
                "Gauge_Type": gauge_types[0],
                "Gauge_Value": gauge_value
            }

            return HttpResponse(json.dumps(gauge_dict), content_type='application/json')
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     return Response(status=status.HTTP_204_NO_CONTENT)
