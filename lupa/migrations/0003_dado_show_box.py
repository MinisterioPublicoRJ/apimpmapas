# Generated by Django 2.2.4 on 2019-09-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lupa', '0002_dado_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='show_box',
            field=models.BooleanField(default=True, verbose_name='Exibir dado'),
        ),
    ]
