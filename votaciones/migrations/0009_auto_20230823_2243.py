# Generated by Django 2.2 on 2023-08-24 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0008_auto_20230823_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrovotostest',
            name='nombre',
            field=models.CharField(default='', max_length=300),
        ),
    ]
