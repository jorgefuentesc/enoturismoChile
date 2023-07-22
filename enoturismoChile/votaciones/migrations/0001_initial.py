# Generated by Django 2.2 on 2023-07-16 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegionesTest',
            fields=[
                ('id', models.BigAutoField(db_column='id_regiones', primary_key=True, serialize=False)),
                ('nombre_regiones', models.CharField(max_length=120)),
                ('regiones_vigencia', models.BooleanField(default=True)),
                ('color', models.CharField(max_length=120)),
                ('color_interior', models.CharField(max_length=120)),
                ('color_circulo', models.CharField(max_length=120)),
            ],
            options={
                'db_table': 'regiones_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VinnasTest',
            fields=[
                ('id', models.BigAutoField(db_column='id_vinnas', primary_key=True, serialize=False)),
                ('nombre_vinna', models.CharField(max_length=120)),
                ('img_url', models.CharField(max_length=120)),
                ('vinnas_vigencia', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'viñas_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VotosUsuarios',
            fields=[
                ('id_usuario_voto', models.BigAutoField(db_column='id_usuario_validacion', primary_key=True, serialize=False)),
                ('pasaporte', models.CharField(max_length=120)),
                ('nombre', models.CharField(max_length=120)),
                ('correo_electronico', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'votos_usuarios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RegistroVotosTest',
            fields=[
                ('id', models.BigAutoField(db_column='id_registros', primary_key=True, serialize=False)),
                ('tipo_registro', models.CharField(max_length=60)),
                ('registro_vigencia', models.BooleanField(default=True)),
                ('validacion_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votaciones.VotosUsuarios')),
                ('vinna', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votaciones.VinnasTest')),
            ],
            options={
                'db_table': 'registro_votos_test',
                'managed': True,
            },
        ),
    ]
