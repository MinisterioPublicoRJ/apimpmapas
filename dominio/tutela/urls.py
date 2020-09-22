from django.urls import path

from .views import (
    ComparadorRadaresView,
    DesarquivamentosView,
    SaidasView,
    EntradasView,
    OutliersView,
    SuaMesaVistasAbertas,
    SuaMesaInvestigacoes,
    SuaMesaProcessos,
    SuaMesaFinalizados,
    SuaMesaDetalheView,
    SuaMesaVistasListaView,
    DetalheAcervoView,
    DetalheProcessosJuizoView,
    TempoTramitacaoView,
    ListaProcessosView,
)
from .radar_views import RadarView


suamesa_urls = [
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
    path(
        'suamesa/detalhe/investigacoes/<str:orgao_id>',
        DetalheAcervoView.as_view(),
        name='suamesa-detalhe-investigacoes'
    ),
    path(
        'suamesa/detalhe/processos/<str:orgao_id>',
        DetalheProcessosJuizoView.as_view(),
        name='suamesa-detalhe-processos'
    ),
    path(
        'suamesa/lista/vistas/<str:orgao_id>/<str:cpf>/<str:abertura>',
        SuaMesaVistasListaView.as_view(),
        name='suamesa-lista-vistas'
    ),
]

stats_urls = [
    path(
        'outliers/<str:orgao_id>',
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
]


urlpatterns = [
    path("radar/<str:orgao_id>", RadarView.as_view(), name="radar"),
    path(
        "desarquivamentos/<str:orgao_id>",
        DesarquivamentosView.as_view(),
        name="desarquivamentos"
    ),
    path(
        "tempo-tramitacao/<str:orgao_id>",
        TempoTramitacaoView.as_view(),
        name="tempo-tramitacao"
    ),
    path(
        "lista/processos/<str:orgao_id>",
        ListaProcessosView.as_view(),
        name="lista-processos"
    ),
    path(
        "comparador-radares/<str:orgao_id>",
        ComparadorRadaresView.as_view(),
        name="tutela-comparador-radares"
    ),
]
urlpatterns += suamesa_urls + stats_urls
