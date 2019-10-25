from django.core.management.base import BaseCommand

from lupa.cache import (_repopulate_cache_data_entity,
                        _repopulate_cache_data_detail,
                        _repopulate_cache_entity)
from lupa.models import Entidade, DadoEntidade, DadoDetalhe
from lupa.serializers import (EntidadeSerializer,
                              DadoEntidadeSerializer,
                              DadoDetalheSerializer)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('obj_type', type=str)

    def handle(self, *args, **options):
        obj_type = options['obj_type']
        if obj_type == 'dado_entidade':
            queryset = DadoEntidade.cache.expiring()
            _repopulate_cache_data_entity(
                'lupa_dado_entidade',
                queryset,
                DadoEntidadeSerializer

            )
        elif obj_type == 'dado_detalhe':
            queryset = DadoDetalhe.cache.expiring()
            _repopulate_cache_data_detail(
                'lupa_dado_detalhe',
                queryset,
                DadoDetalheSerializer

            )

        elif obj_type == 'entidade':
            queryset = Entidade.cache.expiring()
            _repopulate_cache_entity(
                'lupa_entidade',
                queryset,
                EntidadeSerializer
            )
