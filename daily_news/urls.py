from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]

# Enable admin page through environment variable
if settings.ADMIN_ENABLED:
    urlpatterns.append(
        path('admin/', admin.site.urls)
    )