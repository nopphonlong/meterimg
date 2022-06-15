from django.db import models


class Meter(models.Model):
    name = models.CharField(max_length=50)
    Meter_Main_Img = models.ImageField(upload_to='images/')
