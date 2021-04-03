"""team2_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api.views import *




schema_view = get_schema_view(
    openapi.Info(
        title="Team2 Swagger API",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="384817@student.saxion.nl"),
        license=openapi.License(name="Team 2"),
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('test/', test, name='test'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('add_information/', add_information, name='add_information'),
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('dev/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
