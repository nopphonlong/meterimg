from rest_framework import serializers, routers, viewsets
from meterimg.models import Meter
from meterimg.serializers import ImageSerializers


class Imageviewset(viewsets.ModelViewSet):
    serializer_class = ImageSerializers

    queryset = Meter.objects.all()
    serializers_class = ImageSerializers(queryset)


routers = routers.DefaultRouter()
routers.register(r'Image/list', Imageviewset, basename='Image')
