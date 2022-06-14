from django.http import HttpResponse
from django.shortcuts import render, redirect
from form import *


def meter_image_view(request):
    if request.method == 'POST':
        form = MeterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = MeterForm()
    return render(request, 'imgform.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')
