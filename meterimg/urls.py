from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from meterimg import views


router = routers.DefaultRouter()
router.register(r'Images', views.ImageViewset)
router.register(r'JustImages', views.JustImageViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]






