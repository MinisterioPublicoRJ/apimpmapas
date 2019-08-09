# Generated by Django 2.2.2 on 2019-08-08 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20190808_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemaDado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tema do dado')),
            ],
        ),
        migrations.AddField(
            model_name='dado',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_by_theme', to='api.TemaDado', verbose_name='Tema da caixinha'),
        ),
    ]
