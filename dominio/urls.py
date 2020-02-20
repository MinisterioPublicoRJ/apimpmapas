from django.urls import path

from .views import (
    SaidasView,
    EntradasView,
    OutliersView,  # , AlertasListView
    DetalheAcervoView,
)

app_name = 'dominio'

urlpatterns = [
    # path(
    #     'dominio/alertas/<str:orgao_id>',
    #     AlertasListView.as_view(),
    #     name='lista_alertas'
    # ),
    path(
        'detalhe_acervo/'
        '<str:orgao_id>/<str:dt_inicio>/<str:dt_fim>/<str:n>',
        DetalheAcervoView.as_view(),
        name='detalhe_acervo'
    ),
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
    )
]
