from django.urls import path
from votaciones.views import (
    Votaciones,
    ruta_no_encontrada,
    cargar_mdl_vinna
)

app_name = 'votaciones'

urlpatterns = [
    path('categoria', Votaciones.as_view(), name='index'),
    path('cargar_mdl_vinna/', cargar_mdl_vinna, name='cargar_mdl_vinna'),
    path('', ruta_no_encontrada, name='default')
]
