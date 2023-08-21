from django.contrib import admin
from django.urls import path
from votaciones_v_emergente import views

urlpatterns = [
    path('',views.index, name='index'),
    path('cargar_datos_votacion/', views.cargar_datos_votacion, name='cargar_datos_votacion'),
    path('envio_datos_formulario/', views.envio_datos_formulario , name= 'envio_datos_formulario'),
    path('cargar_mdl_vinna/', views.cargar_mdl_vinna, name='cargar_mdl_vinna')
    
]
