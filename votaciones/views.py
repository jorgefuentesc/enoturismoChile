import json
import random
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import   RegionesTest, VinnasTest, RegistroVotosTest
from django.http import HttpResponse, JsonResponse



def index(request):
    # datos = WpqhUsers.objects.all()
    votos_experiencia = RegistroVotosTest.objects.filter(tipo_registro='experienciaENO')
    votos = votos_experiencia.count()
    return render(request,'votacion/index.html',{'votos':votos})




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
    votos_experiencia = RegistroVotosTest.objects.filter(tipo_registro='experienciaENO')
    votos = votos_experiencia.count()
    print(votos)
    # 1 mjr exp
    # 2 vinna emegente
    # tipo_vinna_categoria = VinnasTest.objects.filter(categoria=1)

    for region in regiones:
        if region.regiones_vigencia == 1:
            viñas_de_region = vinnas.filter(region=region, categoria=1)
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
        tipo_registro = 'experienciaENO'


        validacion_pasaporte = RegistroVotosTest.objects.filter(pasaporte=documento).first()
        validacion_correo = RegistroVotosTest.objects.filter(correo_electronico=correo).first()
        registro = RegistroVotosTest.objects.filter(tipo_registro=tipo_registro,pasaporte = documento).first()

        pasaporte = validacion_pasaporte.pasaporte if validacion_pasaporte else None
        correoValidado = validacion_correo.correo_electronico if validacion_correo else None
        registro_validado = registro.tipo_registro if registro else None
        mensaje = ''
        estado = 0
        print("acos")
        if len(viñas_id) >=3:
            if registro_validado and pasaporte:
                estado = 0
                mensaje = ' Voto registrado '
            else:
                for i in range(len(viñas_id)):
                    registro = RegistroVotosTest.objects.create(
                        tipo_registro='experienciaENO',
                        correo_electronico=correo,
                        pasaporte=documento,
                        vinna_id=viñas_id[i],
                        region_id=regiones_id[i],
                    )
                remitente_correo = correo
                asunto_correo = '¡Gracias por votar!'
                # mensaje_html = "<h3>Gracias por votar {{  }}!!!</h3>"
                mensaje_html = f"""
                <html>
	<head>
		<meta http-equiv=”Content-Type” content=”text/html; charset=UTF-8″ />
	</head>
<body>
<table align="center" style="background:#efefef; width: 100%;">
	<td>

	<table width="695" border="0" align="center" cellspacing="0" cellpadding="0" style="font-family:Arial, Helvetica, sans-serif">
	<tr><td><hr style="height: 1px; width: 695px; background-color: #888888; margin: 0px; border: 0px;"></td></tr>
	</table>
	    
<table width="695" border="0" align="center" cellspacing="0" cellpadding="0" style="font-family:Arial, Helvetica, sans-serif; background-color: #000;">
<tr>
	<td style="background-color: rgb(255, 251, 251); padding: 30px; margin-bottom: 30px;"><center><img alt="imagen" src="https://premiosenoturismochile.cl/wp-content/uploads/2023/04/Nuevo-logo-2023-naranjo-1024x572.png" width="150" height="84" style="display: block; border: 0px; margin: 0px;"/></center></td>
	
</tr>
<tr><td><hr style="height: 0px; width: 695px; background-color: #888888; margin: 0px; border: 0px;"></td></tr>
        </table>
		
	<table width="695" border="0" align="center" cellspacing="0" cellpadding="0" style="font-family:Arial, Helvetica, sans-seri">
		<tr style="background-color: #fff;">
		  <td height="100">
		  <ul style="list-style-type:none; margin:0px; border:none;">
		  <li style=" font:museo; font-weight: bold; text-align: justify; font-size:18px; color:#005E7C; padding:20px 40px 0px 0px; margin:0px; line-height: 20px;"><br>Hola {nombre}</li>
		<li style="font:Panton-regular; text-align: justify; font-size:14px; color:#454545; padding:15px 40px 0px 0px; margin:0px; line-height: 20px;">
			Gracias por participar en la votación de los Premios Enoturismo Chile 2023.
			<br><br>
			¡Tus preferencias para la categoría, Mejor Experiencia Enoturistica, han sido registradas exitosamente!.
			<br><br>
			Qué suerte, desde ahora ya te encuentras participando para acceder a una de las fabulosas Experiencias Enoturísticas o Canastas de Productos Regionales que se sortearán en los próximos días.
			<br><br>
			No olvides estar atentos a nuestras redes sociales y enterarte de los resultados de los ganadores de los <a href="https://premiosenoturismochile.cl">#premiosenoturismochile2023</a>.
			<br><br>
			Atentamente, equipo Enoturismo Chile. 
			<br><br>
			<a href="https://premiosenoturismochile.cl">www.premiosenoturismochile.cl</a>
			<br><br>
			<a href="https://www.enoturismochile.cl">www.enoturismochile.cl</a>
		</li>
		<br><br>
		</ul>
		  </td>
		</tr>
		  </table>
		
		<table width="695" border="0" align="center" cellspacing="0" cellpadding="0" style="font-family:Arial, Helvetica, sans-serif; background:#efefef;">
  		<tr>
			<td width="274" style="text-align:center;"><img alt="utem" src="https://premiosenoturismochile.cl/wp-content/uploads/2023/08/footer2-e1692756440961.jpg" /></td>
			
		</tr>
		</table>					
			 
					
		
	</table>
</body>
</html>

                """
                enviar_correo(remitente_correo, asunto_correo, mensaje_html, correo)
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

    link_instagram = vinna.link_instagram if vinna.link_instagram else ''
    link_facebook = vinna.link_facebook if vinna.link_facebook else ''
    link_pagina = vinna.pagina_web if vinna.pagina_web else ''
    link_video = vinna.link_video if vinna.link_video else ''

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