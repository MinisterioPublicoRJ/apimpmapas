# Generated by Django 2.2.4 on 2019-08-15 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lupa', '0033_auto_20190814_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dado',
            name='columns',
        ),
        migrations.RemoveField(
            model_name='mapa',
            name='columns',
        ),
        migrations.AddField(
            model_name='colunadado',
            name='dado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lupa.Dado'),
            preserve_default=False,
        ),
    ]
