from django.urls import path

from .views import (
    SaidasView,
    EntradasView,
    OutliersView,
    SuaMesaVistasAbertas,
    SuaMesaInvestigacoes,
    SuaMesaProcessos,
    SuaMesaFinalizados,
    SuaMesaDetalheView,
    DetalheAcervoView,
    DetalheProcessosJuizoView,
)

app_name = 'dominio'


acervo_patterns = [
    path(
        'detalhe_acervo/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>/<str:n>',
        DetalheAcervoView.as_view(),
        name='detalhe_acervo'
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
        'entradas/<str:orgao_id>/<str:nr_cpf>',
        EntradasView.as_view(),
        name='entradas'
    ),
    path(
        'detalhe_processos/<str:orgao_id>',
        DetalheProcessosJuizoView.as_view(),
        name='detalhe_processos'
    )
]


urlpatterns = acervo_patterns + suamesa_patterns + stats_patterns
