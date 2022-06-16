from rest_framework import serializers
from meterimg.models import Meter


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = ['name', 'Meter_Main_Img']
