# Generated by Django 2.2.2 on 2019-08-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20190801_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='image_column',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]