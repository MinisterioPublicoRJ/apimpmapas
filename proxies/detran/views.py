from django.conf import settings
from django.http import JsonResponse

from proxies.detran.dao import DataTrafficController, HBaseGate, ImpalaGate


def foto_detran_view(request, rg):
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
    return JsonResponse(data=data_controller.get_data())
