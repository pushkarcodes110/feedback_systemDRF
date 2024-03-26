
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('feedback/', include('feedback.api.urls'), name='feedback'),
    path('accounts/', include('accounts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema' ),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    
    
]
