# Librerias
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
import json
import random
import smtplib
import pytz
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db.models import F
# Modelos
from .models import   RegionesTest, VinnasTest, RegistroVotosTest

class Votaciones(View):
    def get(self, request):
        try:
            tipo = request.GET.get('tipo', '')
            regiones = RegionesTest.objects.filter(regiones_vigencia=True)
            vinnas = VinnasTest.objects.all()
            lista_regiones = []

            if tipo == '' or int(tipo) not in [1, 2]:
                return render(request, 'error/404.html')
            
            tipo_registro = 'experienciaENO' if int(tipo) == 1 else 'viñaEmergente'
            print(tipo_registro)
            for region in regiones:
                viñas_de_region = vinnas.filter(region=region, categoria=int(tipo))
                total_votos_regio2n = RegistroVotosTest.objects.filter(region=region, vinna__in=viñas_de_region, tipo_registro=tipo_registro).count()
                
                # Solo si hay viñas en la región actual
                if viñas_de_region:
                    viñas_data = []
                    
                    for viña in viñas_de_region:
                        total_votos_vinna_por_region = RegistroVotosTest.objects.filter(region=region, vinna=viña, tipo_registro=tipo_registro).count()
                        porcentajer = (total_votos_vinna_por_region / total_votos_regio2n) * 100
                        porcentaje = int(porcentajer)
                        
                        viñas_data.append({
                            'nombre_viña': viña.nombre_vinna,
                            'imagen_viña': viña.img_url,
                            'id_viña': viña.id,
                            'porcentaje': porcentaje,
                        })

                    random.shuffle(viñas_data)
                    nombre_viñas, imagen_viñas, id_viñas, porcentajes = zip(*[(vd['nombre_viña'], vd['imagen_viña'], vd['id_viña'], vd['porcentaje']) for vd in viñas_data])
                    print(porcentajes)
                    region_data = {
                        'id_region': region.id,
                        'region': region.nombre_regiones,
                        'viñas': nombre_viñas,
                        'imagenViñas': imagen_viñas,
                        'id_viñas': id_viñas,
                        'colorFondo': region.color,
                        'colorCirculo': region.color_circulo,
                        'colorInterior': region.color_interior,
                        'porcentajes': porcentajes,
                    }

                    lista_regiones.append(region_data)

            random.shuffle(lista_regiones)
            return render(request, 'votaciones/index.html', {'error': False, 'regiones': lista_regiones})
        except Exception as e:
            print('Ocurrió un error, ', e)
            return render(request, 'votaciones/index.html', { 'error': True })

    def post(self, request):
        try:
            # Obtener los datos enviados en el cuerpo de la solicitud JSON
            correo = request.POST.get('correo', None)
            documento = request.POST.get('documento', None)
            nombre = request.POST.get('nombre', None)
            tipo = request.POST.get('tipo_categoria', None)
            opciones = json.loads(request.POST.get('opciones', None))
        
            if correo is None or documento is None or nombre is None or tipo is None or opciones is None:
                return JsonResponse({ 'ok': False, 'mensaje': 'Existen parametros faltantes.' })

            # Obtener solo las viñas
            viñas_id = list(opciones.values())

            # Obtener solo los IDs (regiones)
            regiones_id = list(opciones.keys())

            tipo_registro = 'experienciaENO' if int(tipo) == 1 else 'viñaEmergente'

            zona_horaria = pytz.timezone('America/Santiago')
        
            # Obtener la fecha y hora actuales en la zona horaria de Santiago
            fecha_actual = datetime.now(tz=zona_horaria)
            hora_actual = datetime.now(tz=zona_horaria)
            
            # Formato de fecha "24/08/2023" (día/mes/año)
            formato_hora = "%H:%M"
            formato = "%d/%m/%Y"

            fecha_formateada = fecha_actual.strftime(formato) 
            hora_formateada = hora_actual.strftime(formato_hora)

            voto = RegistroVotosTest.objects.filter(
                pasaporte=documento,
                tipo_registro=tipo_registro,
                registro_vigencia=True
            ).first()

            # Valida si votó
            if(voto): 
                return JsonResponse({ 'ok': False, 'mensaje': 'El rut o pasaporte ingresado ya presenta un voto asociado.'})
            # Valida si la cantidad de votos es igual o superior a 3
            if(len(viñas_id) < 3):
                return JsonResponse({ 'ok': False, 'mensaje': 'Se requieren al menos 3 votos.'})
            # Valida correo electrónico
            expresion_regular = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if(not re.match(expresion_regular, correo)):
                return JsonResponse({ 'ok': False, 'mensaje': 'Correo electrónico inválido.'})
            
            for i in range(len(viñas_id)):
                RegistroVotosTest.objects.create(
                    tipo_registro=tipo_registro,
                    correo_electronico=correo,
                    pasaporte=documento,
                    vinna_id=viñas_id[i],
                    region_id=regiones_id[i],
                    fecha_voto_act=fecha_formateada,
                    hora_voto_act=hora_formateada,
                    nombre=nombre.upper()
                )
            # TODO: ENVIAR CORREO
            return JsonResponse({ 'ok': True, 'mensaje': 'Votos almacenados exitosamente.' })
        except Exception as e:
            return JsonResponse({ 'ok': False, 'mensaje': f"""Ocurrió un error, { e }""" })

def ruta_no_encontrada(request):
    return render(request, 'error/404.html')

def enviar_correo(remitente, asunto, mensaje_html, destinatario):
    # Configura la información del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # El puerto de Gmail para TLS/STARTTLS

    correo_gmail = "enoturismotest@gmail.com"
    contrasena_gmail = "dbdffubzpprpwhfk"
    # contrasena_gmail = "Testeno123"

    if not contrasena_gmail:
        raise ValueError("La variable de entorno GMAIL_APP_PASSWORD no está configurada.")

    # Crea una conexión segura con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Inicia sesión en tu cuenta de Gmail con la "Contraseña de aplicaciones"
    server.login(correo_gmail, contrasena_gmail)

    # Crea el mensaje de correo electrónico en formato MIMEText
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agrega el cuerpo del mensaje como parte del mensaje MIMEText
    msg.attach(MIMEText(mensaje_html, 'html', 'utf-8'))

    # Envía el correo electrónico
    server.sendmail(correo_gmail, destinatario, msg.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit() 

def cargar_mdl_vinna(request):
    vina = request.GET.get('id_vina')
    vinna = VinnasTest.objects.filter(id=vina).first()  # Utiliza 'first()' para obtener solo un objeto, si existe
    nombre_vinna = vinna.nombre_vinna if vinna else None
    titulo_vinna = vinna.vinna_titulo if vinna else None
    descripcion_vinna = vinna.vinna_descripcion if vinna else None
    img_vinna = vinna.vinna_url_img_md if vinna else None

    link_instagram = vinna.link_instagram if vinna else ''
    link_facebook = vinna.link_facebook if vinna else ''
    link_pagina = vinna.pagina_web if vinna else ''
    link_video = vinna.link_video if vinna else ''

    response = {
        'nombre_vinna': nombre_vinna,
        'titulo_vinna': titulo_vinna,
        'descripcion_vinna': descripcion_vinna,
        'img_vinna': img_vinna,
        'link_instagram': link_instagram,
        'link_facebook': link_facebook,
        'link_pagina': link_pagina,
        'link_video': link_video,
    }

    return JsonResponse(response)