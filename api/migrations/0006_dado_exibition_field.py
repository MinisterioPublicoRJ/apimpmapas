# Generated by Django 2.2.2 on 2019-06-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190628_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='exibition_field',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
