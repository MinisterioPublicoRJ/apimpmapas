# Generated by Django 2.2.4 on 2019-09-06 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lupa', '0002_auto_20190821_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dado',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_by_theme', to='lupa.TemaDado', verbose_name='tema da caixinha'),
        ),
    ]
