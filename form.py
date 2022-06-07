from django import forms
from meterimg.models import *


class MeterForm(forms.ModelForm):

	class Meta:
		model = Meter
		fields = ['name', 'hotel_Main_Img']
