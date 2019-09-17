# Generated by Django 2.2.4 on 2019-09-17 20:08

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('cor', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('prioridade', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('image_data', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='icones/mprj_plus/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('visivel', models.BooleanField(default=True)),
                ('fonte_dados', models.TextField()),
                ('tabela_pg', models.CharField(blank=True, max_length=255, null=True)),
                ('tabela_drive', models.CharField(blank=True, max_length=255, null=True)),
                ('subtitulo', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('observacao', models.CharField(blank=True, max_length=255, null=True)),
                ('url_tableau', models.URLField(blank=True, max_length=255, null=True)),
                ('prioridade', models.IntegerField(default=1)),
                ('dados_craai', models.BooleanField(default=True)),
                ('dados_estado', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area_mae', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='temas', to='mprj_plus.Area')),
                ('areas_correlatas', models.ManyToManyField(blank=True, related_name='temas_correlatos', to='mprj_plus.Area')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='icone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mprj_plus.Icone'),
        ),
    ]
