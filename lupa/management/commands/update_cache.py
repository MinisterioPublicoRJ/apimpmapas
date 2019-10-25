from django.core.management.base import BaseCommand

from lupa.cache import _repopulate_cache_data, _repopulate_cache_entity
from lupa.models import Entidade, DadoEntidade
from lupa.serializers import EntidadeSerializer, DadoEntidadeSerializer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('obj_type', type=str)

    def handle(self, *args, **options):
        obj_type = options['obj_type']
        if obj_type == 'dado':
            queryset = DadoEntidade.cache.expiring()
            _repopulate_cache_data(
                'lupa_dado',
                queryset,
                DadoEntidadeSerializer
            )

        elif obj_type == 'entidade':
            queryset = Entidade.cache.expiring()
            _repopulate_cache_entity(
                'lupa_entidade',
                queryset,
                EntidadeSerializer
            )
