from django.urls import include, path
from rest_framework import routers
from meterimg import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'Images', views.ImageViewset)
router.register(r'JustImages', views.JustImageViewset)


urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

urlpatterns = format_suffix_patterns(urlpatterns)




