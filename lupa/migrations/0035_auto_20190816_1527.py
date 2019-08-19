# Generated by Django 2.2.4 on 2019-08-16 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lupa', '0034_auto_20190815_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='colunamapa',
            name='mapa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lupa.Mapa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='colunadado',
            name='info_type',
            field=models.CharField(default='id', help_text='<pre>Toda caixinha e mapa precisa de uma coluna de id\nToda caixinha precisa de uma coluna de dados\nTodo mapa precisa de uma coluna de geojson, contendo a string json de um mapa\nCaixinhas de gráficos precisam de uma coluna do tipo label\nColunas de imagem precisam referenciar um campo do tipo "BLOB"\nColunas de tipo e id de entidade vinculada precisam existir aos pares</pre>', max_length=50, verbose_name='tipo de informação da coluna'),
        ),
        migrations.AlterField(
            model_name='colunamapa',
            name='info_type',
            field=models.CharField(default='id', help_text='<pre>Toda caixinha e mapa precisa de uma coluna de id\nToda caixinha precisa de uma coluna de dados\nTodo mapa precisa de uma coluna de geojson, contendo a string json de um mapa\nCaixinhas de gráficos precisam de uma coluna do tipo label\nColunas de imagem precisam referenciar um campo do tipo "BLOB"\nColunas de tipo e id de entidade vinculada precisam existir aos pares</pre>', max_length=50, verbose_name='tipo de informação da coluna'),
        ),
    ]
