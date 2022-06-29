from django.db import models


class Meter(models.Model):
    name = models.CharField(max_length=50)
    meter_main_img = models.ImageField(upload_to='images/')


class Images(models.Model):
    Images = models.ImageField(upload_to='images_two/')
