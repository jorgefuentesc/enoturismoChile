# Generated by Django 2.2 on 2023-08-24 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0009_auto_20230823_2243'),
    ]

    operations = [       
        migrations.AlterField(
            model_name='registrovotostest',
            name='nombre',
            field=models.CharField(default='sin nombre', max_length=300),
        ),
    ]