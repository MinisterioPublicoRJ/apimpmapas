from django.urls import path

from .views import (
    AcervoView,
    SaidasView,
    EntradasView,
    AcervoVariationView,
    AcervoVariationTopNView,
    OutliersView,
    SuaMesaVistasAbertas,
    SuaMesaInvestigacoes,
    SuaMesaProcessos,
    SuaMesaFinalizados,
    SuaMesaDetalheView,
)

app_name = 'dominio'


acervo_patterns = [
    path(
        'acervo/<str:orgao_id>/<str:data>',
        AcervoView.as_view(),
        name='acervo'
    ),
    path(
        'acervo_variation/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>',
        AcervoVariationView.as_view(),
        name='acervo_variation'
    ),
    path(
        'acervo_variation_topn/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>/<str:n>',
        AcervoVariationTopNView.as_view(),
        name='acervo_variation_topn'
    ),
]


suamesa_patterns = [
    path(
        'suamesa/vistas/<str:orgao_id>/<str:cpf>',
        SuaMesaVistasAbertas.as_view(),
        name='suamesa-vistas'
    ),
    path(
        'suamesa/investigacoes/<str:orgao_id>',
        SuaMesaInvestigacoes.as_view(),
        name='suamesa-investigacoes'
    ),
    path(
        'suamesa/processos/<str:orgao_id>',
        SuaMesaProcessos.as_view(),
        name='suamesa-processos'
    ),
    path(
        'suamesa/finalizados/<str:orgao_id>',
        SuaMesaFinalizados.as_view(),
        name='suamesa-finalizados'
    ),
    path(
        'suamesa/detalhe/vistas/<str:orgao_id>/<str:cpf>',
        SuaMesaDetalheView.as_view(),
        name='suamesa-detalhe-vistas'
    ),
]


stats_patterns = [
    path(
        'outliers/'
        '<str:orgao_id>/<str:dt_calculo>',
        OutliersView.as_view(),
        name='outliers'
    ),
    path(
        'saidas/<str:orgao_id>',
        SaidasView.as_view(),
        name='saidas'
    ),
    path(
        'entradas/<str:orgao_id>/<str:cod_matricula>',
        EntradasView.as_view(),
        name='entradas'
    ),
]


urlpatterns = acervo_patterns + suamesa_patterns + stats_patterns
