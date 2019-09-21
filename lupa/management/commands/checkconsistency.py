from django.core.management.base import BaseCommand, CommandError
from lupa.models import Dado, Entidade
from lupa.db_connectors import execute



class Command(BaseCommand):
    help = 'Verififca a integridade mínima das views usadas pelo Lupa'

    def printok(self, message, end='\n'):
        self.stdout.write(self.style.SUCCESS(message), ending=end)

    def printnok(self, message, exception=None, end="\n"):
        self.stdout.write(self.style.ERROR(message), ending=end)
    
    def printstatus(self, message, end="\n"):
        self.stdout.write(message, ending=end)

    def add_arguments(self, parser):
        parser.add_argument('entity_id', type=int)

    def handle(self, *args, **options):
        entity_id = options['entity_id']

        dados = Dado.objects.filter(entity_type__id=entity_id)
        entidade = Entidade.objects.get(id=entity_id)

        self.printstatus("Verificando Dado(caixinhas) para entidade %s" % entidade)
        for dado in dados:
            self.printstatus("Dado: %s id=%s - " % (dado, dado.id), end=' ')
            columns = dado.column_list.all()
            columns = ['%s as %s' % (column.name, column.info_type) for column in columns]
            try:
                retorno = execute(
                    dado.database,
                    dado.schema,
                    dado.table,
                    columns,
                    None,
                    None,
                    True
                )
                self.printok('OK', end='')
                retcount = len(retorno)
                if not retcount:
                    self.printnok(' SEM RESULTADOS')
                else:
                    self.printok('')
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
