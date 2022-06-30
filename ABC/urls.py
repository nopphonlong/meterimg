"""ABC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.db import router
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from meterimg.views import *
from meterimg.urls import router
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = [
                  path('api_schema', get_schema_view(title='API Schema', description='All API'), name='api_schema'),
                  path('tests/', test),
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  path('swagger-ui/', TemplateView.as_view(
                      template_name='docs.html',
                      extra_context={'schema_url': 'api_schema'}
                  ), name='swagger-ui'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
