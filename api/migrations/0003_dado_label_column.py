# Generated by Django 2.2.2 on 2019-07-23 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190723_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='label_column',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
