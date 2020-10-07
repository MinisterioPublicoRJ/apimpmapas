from django.urls import path

from .views import (
    ComparadorRadaresView,
    RadarView,
    DesarquivamentosView,
    SaidasView,
    EntradasView,
    OutliersView,
    SuaMesaDetalheView,
    SuaMesaVistasListaView,
    TempoTramitacaoView,
    ListaProcessosView,
)


suamesa_urls = [
    path(
        'suamesa/detalhe/vistas/<str:orgao_id>/<str:cpf>',
        SuaMesaDetalheView.as_view(),
        name='suamesa-detalhe-vistas'
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
