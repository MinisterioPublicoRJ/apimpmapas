from django.conf import settings

from dominio.dao import GenericDAO
from dominio.alertas.serializers import AlertasComprasSerializer


class GenericAlertasDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "alertas", "queries")


class AlertaComprasDAO(GenericAlertasDAO):
    query_file = "alerta_compras.sql"
    columns = [
        "sigla",
        "contrato",
        "iditem",
        "contrato_iditem",
        "item"
    ]
    serializer = AlertasComprasSerializer
    table_namespaces = {"schema": settings.TABLE_NAMESPACE}

    # Para fazer executando a query simplesmente deletar esse metodo override
    @classmethod
    def execute(cls, **kwargs):
        dummy_result = [
            ('COMP', '2020001923', '58818', '2020001923-58818',
             ('MASCARA CIRURGICA DESCARTAVEL - MATERIAL MASCARA: TECIDO NAO T'
              'ECIDO, QUANTIDADE CAMADA: 3, CLIP NASAL: METALICO, FORMATO: SIM'
              'PLES (RETANGULAR), MATERIAL VISOR: N/A, GRAMATURA: 30 G/MÃ‚Â², '
              'FILTRO: N/D, FIXACAO: AMARRAS, COR: N/D')
             ),
            ('COMP', '2020101010', '12345', '2020101010-12345',
             'LUVA COMESTIVEL DE TESTE')]
        return dummy_result
