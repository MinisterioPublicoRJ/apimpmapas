# Generated by Django 2.2.4 on 2019-10-16 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lupa', '0006_auto_20191016_1735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dadodetalhe',
            options={'ordering': ('order',)},
        ),
    ]
