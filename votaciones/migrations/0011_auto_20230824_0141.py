# Generated by Django 2.2 on 2023-08-24 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0010_auto_20230824_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrovotostest',
            name='nombre',
        ),
        
    ]
