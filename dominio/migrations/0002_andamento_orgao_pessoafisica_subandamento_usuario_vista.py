# Generated by Django 2.2.2 on 2020-03-23 15:43

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('dominio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Andamento',
            fields=[
                ('pcao_dk', models.IntegerField(primary_key=True, serialize=False)),
                ('pcao_dt_andamento', models.DateField(db_column='PCAO_DT_ANDAMENTO')),
            ],
            options={
                'db_table': 'MCPR_ANDAMENTO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orgao',
            fields=[
                ('orgi_dk', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='ORGI_NM_ORGAO', max_length=145)),
            ],
            options={
                'db_table': 'ORGI_ORGAO',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PessoaFisica',
            fields=[
                ('pesf_pess_dk', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='PESF_NM_PESSOA_FISICA', max_length=145, null=True)),
                ('cpf', models.CharField(db_column='PESF_CPF', max_length=11, null=True)),
            ],
            options={
                'db_table': 'MCPR_PESSOA_FISICA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubAndamento',
            fields=[
                ('stao_dk', models.IntegerField(primary_key=True, serialize=False)),
                ('stao_tppr_dk', models.IntegerField(db_column='STAO_TPPR_DK')),
            ],
            options={
                'db_table': 'MCPR_SUB_ANDAMENTO',
                'managed': False,
            },
            managers=[
                ('finalizados', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Vista',
            fields=[
                ('vist_dk', models.IntegerField(primary_key=True, serialize=False)),
                ('data_fechamento', models.DateField(db_column='VIST_DT_FECHAMENTO_VISTA', null=True)),
                ('data_abertura', models.DateField(db_column='VIST_DT_ABERTURA_VISTA')),
            ],
            options={
                'db_table': 'MCPR_VISTA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('last_login', models.DateField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
