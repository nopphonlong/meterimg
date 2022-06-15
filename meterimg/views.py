from meterimg.models import Meter
from meterimg.serializers import ImageSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


class ImageViewset(viewsets.ModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = ImageSerializers


