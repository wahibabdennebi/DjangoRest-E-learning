
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Abonne.urls')),
    path('auth/', include('accounts.urls')),
    path(r'^auth/', include('djoser.urls')),
    path(r'^auth/', include('djoser.urls.jwt'))
]
