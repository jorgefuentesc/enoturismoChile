from django.db import models

# class WpqhUsers(models.Model):
#     id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     user_login = models.CharField(max_length=60)
#     user_pass = models.CharField(max_length=255)
#     user_nicename = models.CharField(max_length=50)
#     user_email = models.CharField(max_length=100)
#     user_url = models.CharField(max_length=100)
#     user_registered = models.DateTimeField()
#     user_activation_key = models.CharField(max_length=255)
#     user_status = models.IntegerField()
#     display_name = models.CharField(max_length=250)
#     class Meta:
#         managed = False
#         db_table = 'wpqh_users'

class VotosUsuarios(models.Model):
    id_usuario_voto = models.BigAutoField(db_column='id_usuario_validacion', primary_key=True) 
    pasaporte = models.CharField(max_length=120)
    nombre = models.CharField(max_length=120)
    correo_electronico = models.CharField(max_length=100)
    class Meta:
        managed = True
        db_table = 'votos_usuarios'

class RegionesTest(models.Model):
    id = models.BigAutoField(db_column='id_regiones', primary_key=True)
    nombre_regiones = models.CharField(max_length=120)
    regiones_vigencia = models.BooleanField(default=True)
    color = models.CharField(max_length=120)
    color_interior = models.CharField(max_length=120)
    color_circulo = models.CharField(max_length=120)
    class Meta:
        managed = False
        db_table = 'regiones_test'

class VinnasTest(models.Model):
    id = models.BigAutoField(db_column='id_vinnas', primary_key=True)
    nombre_vinna = models.CharField(max_length=120)
    img_url = models.CharField(max_length=120)
    region = models.ForeignKey(RegionesTest, blank=True,null=True, on_delete=models.CASCADE)
    vinnas_vigencia = models.BooleanField(default=True)
    vinna_url_img_md = models.CharField(max_length=200, default='https://st.depositphotos.com/1000423/60623/i/600/depositphotos_606236826-stock-photo-nanotechnology-molecule-and-atom-model.jpg')
    vinna_descripcion = models.CharField(max_length=120,default='Aqui va una breve descripción de la viña, ejemplo donde esta ubicada y demas')
    vinna_titulo = models.CharField(max_length=120,default='Titulo viña')
    class Meta:
        managed = True
        db_table = "viñas_test"

class RegistroVotosTest(models.Model):
    id = models.BigAutoField(db_column='id_registros', primary_key=True)
    tipo_registro = models.CharField(max_length=60)
    registro_vigencia = models.BooleanField(default=True)
    correo_electronico = models.CharField(max_length=120, default='correo@example.com')
    pasaporte = models.CharField(max_length=120, default='1111111')
    vinna = models.ForeignKey(VinnasTest,blank=True,null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(RegionesTest,blank=True,null=True, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = "registro_votos_test"


