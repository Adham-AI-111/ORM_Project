from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('api.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]+ debug_toolbar_urls()
