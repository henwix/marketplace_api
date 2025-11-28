from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # v1 api endpoints
    path('v1/', include('src.api.v1.urls')),
]


if settings.DEBUG:
    urlpatterns.extend(
        [
            path('silk/', include('silk.urls', namespace='silk')),
        ],
    )
