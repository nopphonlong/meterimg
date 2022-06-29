from rest_framework import serializers
from meterimg.models import Meter, Images


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = ['name', 'meter_main_img']


class JustimageimageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['Images']
