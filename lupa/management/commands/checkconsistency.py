from django.core.management.base import BaseCommand
from lupa.models import DadoEntidade, Entidade
from lupa.db_connectors import execute_sample
from lupa.logging import Log


def parsecolumns(columns):
    return [
        '%s as %s' % (column.name, column.info_type)
        for column in columns
    ]


class Command(BaseCommand):
    help = 'Verifica a integridade mínima das views usadas pelo Lupa'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log = Log()

    def printok(self, message, end='\n'):
        self._log.printok(message, ending=end)

    def printnok(self, message, exception=None, end="\n"):
        self._log.printerr(message, ending=end)

    def printstatus(self, message, end="\n"):
        self._log.print(message, ending=end)

    def add_arguments(self, parser):
        parser.add_argument('entity_id', type=int)

    def process_execution(self, dado, columns):
        retorno = execute_sample(
            dado.database,
            dado.schema,
            dado.table,
            columns
        )
        self.printok('OK', end='')
        retcount = len(retorno)
        if not retcount:
            self.printnok(' SEM RESULTADOS')
        else:
            self.printok('')

    def process_data(self, dado):
        self.printstatus(f'Dado: {dado} id={dado.id} - ', end=' ')
        columns = dado.column_list.all()
        columns = parsecolumns(columns)
        try:
            self.process_execution(dado, columns)
            if hasattr(dado, 'data_details'):
                for detalhe in dado.data_details.all().order_by('id'):
                    self.process_data(detalhe)
        except Exception as error:
            self.printnok(
                'NOK - %s' %
                ' - '.join(
                    [
                        dado.database,
                        dado.schema,
                        dado.table
                    ]
                ),
                error
            )

    def handle(self, *args, **options):
        entity_id = options['entity_id']
        dados = DadoEntidade.objects.filter(entity_type__id=entity_id)
        entidade = Entidade.objects.get(id=entity_id)

        self.printstatus(
            "Verificando Dado(caixinhas) para entidade %s" % entidade
        )
        list(map(self.process_data, dados))
