
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('votaciones.urls'), name='votaciones'),
    path('vinna_emergente/',include('votaciones_v_emergente.urls'), name='votaciones_e'),
]
