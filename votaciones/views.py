import json
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.shortcuts import render, redirect
from .models import   RegionesTest, VinnasTest, RegistroVotosTest
from django.http import HttpResponse, JsonResponse
import pytz
from datetime import datetime



def index(request):
    # datos = WpqhUsers.objects.all()
    votos_experiencia = RegistroVotosTest.objects.filter(tipo_registro='experienciaENO')
    votos = votos_experiencia.count()
    return render(request,'votacion/index.html',{'votos':votos})

def enviar_correo(asunto, mensaje_html, destinatario):
    # Configura la información del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # El puerto de Gmail para TLS/STARTTLS

    # Crea una conexión segura con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Inicia sesión en tu cuenta de Gmail con la "Contraseña de aplicaciones"
    server.login(settings.EMAIL, settings.PASSWORD_EMAIL)

    # Crea el mensaje de correo electrónico en formato MIMEText
    msg = MIMEMultipart()
    msg['From'] = 'ENOTURISMO'
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agrega el cuerpo del mensaje como parte del mensaje MIMEText
    msg.attach(MIMEText(mensaje_html, 'html', 'utf-8'))

    # Envía el correo electrónico
    server.sendmail(settings.EMAIL, destinatario, msg.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit() 

def cargar_datos_votacion(request):
    response = { 'ok': False }

    try:
        regiones = RegionesTest.objects.all()
        vinnas = VinnasTest.objects.all()
        lista_regiones = []
        votos_experiencia = RegistroVotosTest.objects.filter(tipo_registro='experienciaENO')
        votos = votos_experiencia.count()
        tipo_registro = 'experienciaENO'
        for region in regiones:
            viñas_de_region = vinnas.filter(region=region, categoria=1)
            # Solo si hay viñas en la región actual
            if viñas_de_region:
                viñas_data = []
                for viña in viñas_de_region:
                    viñas_data.append({
                        'nombre_viña': viña.nombre_vinna,
                        'imagen_viña': viña.img_url,
                        'id_viña': viña.id,
                    })
                random.shuffle(viñas_data)
                nombre_viñas, imagen_viñas, id_viñas = zip(*[(vd['nombre_viña'], vd['imagen_viña'], vd['id_viña']) for vd in viñas_data])
                region_data = {
                    'id_region': region.id,
                    'region': region.nombre_regiones,
                    'viñas': nombre_viñas,
                    'imagenViñas': imagen_viñas,
                    'id_viñas': id_viñas,
                    'colorFondo': region.color,
                    'colorCirculo': region.color_circulo,
                    'colorInterior': region.color_interior,
                    'votos_cantidad_experiencia':votos,
                }
                lista_regiones.append(region_data)
        random.shuffle(lista_regiones)  # Esto reorganizará las regiones de manera aleatoria también
        response = { 'ok': True, 'data': lista_regiones }
    except Exception as e:
        response = { 'ok': False, 'error': e }
    return JsonResponse(response, safe=False)

def envio_datos_formulario(request):
    if request.method == 'POST':
        # Se recupera navegador e ip de usuario que vota
        browser = request.META.get('HTTP_USER_AGENT')
        ip_votante = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get('HTTP_X_FORWARDED_FOR') is not None else request.META.get('REMOTE_ADDR')
        # Obtener los datos enviados en el cuerpo de la solicitud JSON
        data = json.loads(request.body)
        correo = data.get('correo', None)
        documento = data.get('documento', None)
        nombre = data.get('nombre', None)
        opciones = data.get('opciones', {})
        # Obtener solo las viñas
        viñas_id = list(opciones.values())
        # Obtener solo los IDs (regiones)
        regiones_id = list(opciones.keys())
        tipo_registro = 'experienciaENO'
        
        zona_horaria = pytz.timezone('America/Santiago')
    
        # Obtener la fecha y hora actuales en la zona horaria de Santiago
        fecha_actual = datetime.now(tz=zona_horaria)
        hora_actual = datetime.now(tz=zona_horaria)
        
        # Formato de fecha "24/08/2023" (día/mes/año)
        formato_hora = "%H:%M"
        formato = "%d/%m/%Y"

        fecha_formateada = fecha_actual.strftime(formato) 
        hora_formateada = hora_actual.strftime(formato_hora)

        validacion_pasaporte = RegistroVotosTest.objects.filter(pasaporte=documento).first()
        validacion_correo = RegistroVotosTest.objects.filter(correo_electronico=correo).first()
        registro = RegistroVotosTest.objects.filter(tipo_registro=tipo_registro,pasaporte = documento).first()

        pasaporte = validacion_pasaporte.pasaporte if validacion_pasaporte else None
        correoValidado = validacion_correo.correo_electronico if validacion_correo else None
        registro_validado = registro.tipo_registro if registro else None
        mensaje = ''
        estado = 0

        if len(viñas_id) >=3:
            if registro_validado and pasaporte:
                estado = 0
                mensaje = ' el rut asociado al voto ya fue registrado anteriormente '
            else:
                for i in range(len(viñas_id)):
                    registro = RegistroVotosTest.objects.create(
                        tipo_registro='experienciaENO',
                        correo_electronico=correo,
                        pasaporte=documento,
                        vinna_id=viñas_id[i],
                        region_id=regiones_id[i],
                        fecha_voto_act=fecha_formateada,
                        hora_voto_act=hora_formateada,
                        nombre=nombre.upper(),
                        ip_votante=ip_votante,
                        browser=browser
                    )
                mensaje = 'Votacion exitosa.'
                estado = 1
        else:
            mensaje = ' Cantidad de votos insuficientes, debes seleccionar como minimo tres de diferentes empresas. '
            estado = 0
        response_data = {
            'message': mensaje,
            'data': estado,
        }
        return JsonResponse(response_data)
    
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

    response = {'nombre_vinna': nombre_vinna,
                'titulo_vinna': titulo_vinna,
                'descripcion_vinna': descripcion_vinna,
                'img_vinna': img_vinna,
                'link_instagram': link_instagram,
                'link_facebook': link_facebook,
                'link_pagina': link_pagina,
                'link_video': link_video,
                }
    return JsonResponse(response)
