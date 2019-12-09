from decouple import config
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from busca_desaparecidos.dao import client, search_target_person

from desaparecidos.tasks import async_calculate_rank


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        id_sinalid = kwargs.pop('id_sinalid')
        cursor = client(
            config('DESAPARECIDOS_DB_USER'),
            config('DESAPARECIDOS_DB_PWD'),
            config('DESAPARECIDOS_DB_HOST')
        )
        person = search_target_person(cursor, id_sinalid)
        if person is None:
            data, status\
                = {'status': 'Identificador Sinalid não encontrado'}, 404
        else:
            data, status = cache.get(id_sinalid), 200

        if data is None:
            async_calculate_rank.delay(id_sinalid, person)
            cache.set(id_sinalid, {'status': 'processing'})
            data, status = {'status': 'Seu pedido será processado'}, 201

        return Response(data, status=status)
