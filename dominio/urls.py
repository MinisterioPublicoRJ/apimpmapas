from django.urls import path
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token


from .views import (
    login,
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
)
from dominio.radar_views import SuaPromotoriaView


app_name = 'dominio'


jwt_patterns = [
    path('token/login/', login),
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
]


radar_patterns = [
    path(
        "radar/<str:orgao_id>",
        SuaPromotoriaView.as_view(),
        name="radar"
    ),
]


urlpatterns = suamesa_patterns + stats_patterns + radar_patterns + jwt_patterns
