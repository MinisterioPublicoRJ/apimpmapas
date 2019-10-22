from django.core.management.base import BaseCommand

from lupa.cache import _repopulate_cache_data, _repopulate_cache_entity
from lupa.models import Dado, Entidade
from lupa.serializers import DadoSerializer, EntidadeSerializer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('obj_type', type=str)

    def handle(self, *args, **options):
        obj_type = options['obj_type']
        if obj_type == 'dado':
            queryset = Dado.cache.expiring()
            _repopulate_cache_data(
                'lupa_dado',
                queryset,
                DadoSerializer
            )

        elif obj_type == 'entidade':
            queryset = Entidade.cache.expiring()
            _repopulate_cache_entity(
                'lupa_entidade',
                queryset,
                EntidadeSerializer
            )
