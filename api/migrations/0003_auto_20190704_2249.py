# Generated by Django 2.2.2 on 2019-07-04 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190704_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='schema',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dado',
            name='table',
            field=models.CharField(max_length=100),
        ),
    ]
