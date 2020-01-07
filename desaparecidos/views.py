from decouple import config
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from busca_desaparecidos.dao import client, search_target_person

from desaparecidos.tasks import async_calculate_rank
from desaparecidos.utils import paginate, previous_next_page


def _client():
    return client(
        config('DESAPARECIDOS_DB_USER'),
        config('DESAPARECIDOS_DB_PWD'),
        config('DESAPARECIDOS_DB_HOST')
    )


def page_to_int(func):
    def inner(*args, **kwargs):
        try:
            page = int(kwargs.pop('page'))
        except ValueError:
            page = 1

        return func(page=page, *args, **kwargs)

    return inner


@page_to_int
def _paginate(data, page):
    page_size = config('DESAPARECIDOS_PAGE_SIZE', cast=int)
    return paginate(data, page=page, page_size=page_size)


@page_to_int
def _links(request, page):
    base_url = '{scheme}://{host}{path}'.format(
        scheme=request.scheme,
        host=request.META.get('HTTP_HOST', 'localhost.com'),
        path=request.path
    )
    return previous_next_page(
        base_url,
        page=page,
        data_len=config('DESAPARECIDOS_DATA_LEN', cast=int),
        page_size=config('DESAPARECIDOS_PAGE_SIZE', cast=int),
    )


class DesaparecidosView(APIView):
    def get(self, request, *args, **kwargs):
        id_sinalid = kwargs.pop('id_sinalid')
        cursor = _client()
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

        if data['status'] == 'ready':
            page = request.GET.get('page', 1)
            data['data'] = _paginate(data['data'], page=page)
            data['_links'] = _links(request, page=page)

        return Response(data, status=status)
