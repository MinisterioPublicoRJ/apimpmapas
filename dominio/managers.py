from datetime import date

from django.db import models
from django.db.models import Q


class VistaManager(models.Manager):
    def abertas(self):
        return self.get_queryset().filter(
            Q(data_fechamento=None) |
            Q(data_fechamento__gt=date.today())
        )

    def abertas_promotor(self, orgao_id, cpf):
        """Busca o número de vistas abertas para um dado órgão e matrícula
        na base do Oracle.

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.

        Returns:
            List[Tuple] -- Lista com o resultado da query.
        """
        return self.abertas().filter(orgao=orgao_id, responsavel__cpf=cpf)
