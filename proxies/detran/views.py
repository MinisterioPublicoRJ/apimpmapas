from django.conf import settings
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from proxies.detran.dao import DataTrafficController, HBaseGate, ImpalaGate
from proxies.exceptions import (
    DataDoesNotExistException,
    DetranAPIClientError,
    ServiceUnavailableAPIException,
    WaitDBException,
)


class FotoDetranView(APIView):
    def start_controller(self, rg):
        hbase_gate = HBaseGate(
            table_name=settings.HBASE_DETRAN_BASE,
            server=settings.HBASE_SERVER,
            timeout=settings.HBASE_TIMEOUT,
        )
        impala_gate = ImpalaGate(table_name=settings.IMPALA_DETRAN_TABLE)
        data_controller = DataTrafficController(
            rg=rg, data_dao=impala_gate, photo_dao=hbase_gate,
        )
        return data_controller

    def get(self, request, *args, **kwargs):
        rg = kwargs.get("rg")

        data_controller = self.start_controller(rg)
        try:
            data = data_controller.get_data()
        except DetranAPIClientError:
            raise ServiceUnavailableAPIException(
                detail="Serviço do Detran temporariamente indisponível",
                code="detran_service_unavailable",
            )
        except DataDoesNotExistException:
            raise NotFound(detail=f"Dado não encontrado para RG: {rg}")
        except WaitDBException:
            raise ServiceUnavailableAPIException(
                detail="Tempo de busca dos dados excedeu o tempo máximo",
                code="db_persist_timeout",
            )

        return Response(data=data)
