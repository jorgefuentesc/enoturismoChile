# Generated by Django 2.2 on 2023-09-21 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrovotostest',
            name='browser',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registrovotostest',
            name='ip_votante',
            field=models.TextField(blank=True, null=True),
        ),
    ]
