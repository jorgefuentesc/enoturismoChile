# Generated by Django 2.2 on 2023-08-21 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0005_auto_20230725_1759'),
    ]

    operations = [

        migrations.AlterField(
            model_name='vinnastest',
            name='vinna_descripcion',
            field=models.TextField(default='Aqui va una breve descripción de la viña, ejemplo donde esta ubicada y demas', max_length=120),
        ),
    ]
