from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from proxies.detran.dao import DataTrafficController, HBaseGate, ImpalaGate
from proxies.exceptions import (
    DetranAPIClientError,
    ServiceUnavailableAPIException,
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
            rg=rg,
            data_dao=impala_gate,
            photo_dao=hbase_gate,
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

        return JsonResponse(data=data)
