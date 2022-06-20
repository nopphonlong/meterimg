from meterimg.models import Meter, Images
from meterimg.serializers import ImageSerializers, JustimageimageSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


class ImageViewset(viewsets.ModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = ImageSerializers


class JustImageViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = JustimageimageSerializers
