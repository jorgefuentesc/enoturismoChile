from django.shortcuts import render

# Create your views here.
import json
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from votaciones.models import RegionesTest, VinnasTest, RegistroVotosTest
from django.http import HttpResponse, JsonResponse



def index(request):
    votos_experiencia = RegistroVotosTest.objects.filter(tipo_registro='viñaEmergente')
    votos = votos_experiencia.count()
    return render(request,'votacion_emergente/index.html',{'votos':votos})




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

def cargar_datos_votacion(request):
    regiones = RegionesTest.objects.all()
    vinnas = VinnasTest.objects.all()
    lista_regiones = []
    votos_emergente = RegistroVotosTest.objects.filter(tipo_registro='viñaEmergente')
    votos = votos_emergente.count() if votos_emergente else 0
    print(votos)

    for region in regiones:
        if region.regiones_vigencia == 1:
            viñas_de_region = vinnas.filter(region=region, categoria=2)
            if viñas_de_region:
                viñas_data = list(zip([viña.nombre_vinna for viña in viñas_de_region],
                                [viña.img_url for viña in viñas_de_region],
                                [viña.id for viña in viñas_de_region]))
            
                random.shuffle(viñas_data)  # Reorganizar la lista de viñas aleatoriamente  
                
                if viñas_data:
                    nombre_viñas, imagen_viñas, id_viñas = zip(*viñas_data)   
                else:
                    print("datos insuficifientes")
                region_data = {
                    'id_region': region.id,
                    'region': region.nombre_regiones,
                    'viñas': nombre_viñas,
                    'imagenViñas': imagen_viñas,
                    'id_viñas': id_viñas,
                    'colorFondo': region.color,
                    'colorCirculo': region.color_circulo,
                    'colorInterior': region.color_interior,
                    'votos_cantidad_experiencia':votos
                }
                lista_regiones.append(region_data)

    random.shuffle(lista_regiones)  # Esto reorganizará las regiones de manera aleatoria también
    return JsonResponse(lista_regiones, safe=False)

def envio_datos_formulario(request):
    if request.method == 'POST':
        
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
        tipo_registro = 'viñaEmergente'


        validacion_pasaporte = RegistroVotosTest.objects.filter(pasaporte=documento).first()
        validacion_correo = RegistroVotosTest.objects.filter(correo_electronico=correo).first()
        registro = RegistroVotosTest.objects.filter(tipo_registro=tipo_registro,pasaporte = documento ).first()

        pasaporte = validacion_pasaporte.pasaporte if validacion_pasaporte else None
        correoValidado = validacion_correo.correo_electronico if validacion_correo else None
        registro_validado = registro.tipo_registro if registro else None
        mensaje = ''
        estado = 0
        print(registro_validado,"aquiiiiis")

        if len(viñas_id) >=3:
            if registro_validado and pasaporte:
                estado = 0
                mensaje = ' Voto registrado '
            else:
                for i in range(len(viñas_id)):
                    registro = RegistroVotosTest.objects.create(
                        tipo_registro='viñaEmergente',
                        correo_electronico=correo,
                        pasaporte=documento,
                        vinna_id=viñas_id[i],
                        region_id=regiones_id[i],
                    )
                remitente_correo = correo
                asunto_correo = '¡Gracias por votar!'
                mensaje_html = f"""
                <html>
                <head></head>
                <body>
                <p>Hola {nombre} !!!</p>
                <p>Gracias por participar en la votación.</p>
                <p>¡Tu voto: {tipo_registro}, ha sido registrado exitosamente!</p>
                <p>Esperamos que esta experiencia haya sido de tu agrado!.</p>
                <p>Atentamente,<br>El equipo de Votaciones</p>
                </body>
                </html>
                """
                enviar_correo(remitente_correo, asunto_correo, mensaje_html, correo)
                mensaje = 'Votacion exitosa.'
                estado = 1
        else:
            mensaje = ' cantidad de votos insuficientes, por favor leer instrucciones. '
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
    response = {'nombre_vinna': nombre_vinna,
                'titulo_vinna': titulo_vinna,
                'descripcion_vinna': descripcion_vinna,
                'img_vinna': img_vinna,
                }
    return JsonResponse(response)