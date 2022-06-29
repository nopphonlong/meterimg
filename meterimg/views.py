from meterimg.models import Meter, Images
from meterimg.serializers import ImageSerializers, JustimageimageSerializers
from rest_framework import permissions, viewsets, mixins, status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gauge_reader_main.models.Gauge_classification import getpredict
from gauge_reader_main.models.guage_reading import get_gauge_value
import json


class ImageViewset(viewsets.ModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = ImageSerializers


class JustImageViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = JustimageimageSerializers


@api_view(['GET', 'POST'])
def test(request, format=None):
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
            value = getpredict(img_path)
            # print(value)
            print(f"Predicted Class: {value[0]}, {value[1]:0.2f}%\n")
            print(f"Gauge reading value: {get_gauge_value(img_path, min_value=-1, max_value=3, scale_width=0.5, scale_height=0.5):.2f} bar")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
