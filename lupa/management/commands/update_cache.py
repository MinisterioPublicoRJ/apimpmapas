from django.core.management.base import BaseCommand

from lupa.cache import (_repopulate_cache_data_entity,
                        _repopulate_cache_data_detail,
                        _repopulate_cache_entity,
                        ENTITY_KEY_PREFIX,
                        DATA_ENTITY_KEY_PREFIX,
                        DATA_DETAIL_KEY_PREFIX
                        )
from lupa.models import Entidade, DadoEntidade, DadoDetalhe


class CacheOption:
    def __init__(self, option):
        self._obj, self._prefix, self._action = self.pre_init(option)

    def pre_init(self, option):
        options = {
            'entidade': (
                Entidade,
                ENTITY_KEY_PREFIX,
                _repopulate_cache_entity
            ),
            'dado_entidade': (
                DadoEntidade,
                DATA_ENTITY_KEY_PREFIX,
                _repopulate_cache_data_entity
            ),
            'dado_detalhe': (
                DadoDetalhe,
                DATA_DETAIL_KEY_PREFIX,
                _repopulate_cache_data_detail
            )
        }

        if option not in options:
            raise ValueError(
                'Opção "%s" inválida. Escolha entre: %s'
                % (option, list(options))
            )

        return options[option]

    def queryset(self):
        return self._obj.cache.expiring()

    def repopulate(self):
        self._action(self._prefix, self.queryset())


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('obj_type', type=str)

    def handle(self, *args, **options):
        cache_option = CacheOption(options['obj_type'])
        cache_option.repopulate()
