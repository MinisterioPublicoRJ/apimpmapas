from datetime import date

from django.db import models
from django.db.models import (
    Case,
    Q,
    F,
    ExpressionWrapper,
    Value,
    Sum,
    When
)


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
        return self.abertas().filter(
            Q(documento__docu_orgi_orga_dk_responsavel=orgao_id) |
            Q(documento__docu_orgi_orga_dk_carga=orgao_id),
            responsavel__cpf=cpf
        ).exclude(documento__docu_tpst_dk=11)

    def abertas_por_dias_abertura(self, orgao_id, cpf):
        """
        Busca o número de vistas abertas para um um dado órgão e matrícula
        agrupadas com a contagem de dias que estão abertas

        Arguments:
            orgao_id {integer} -- ID do órgão a ser procurado.
            cpf {String} -- cpf do usuário detentor das vistas.
        """

        queryset = self.abertas_promotor(orgao_id, cpf).annotate(
            dias_abertura=ExpressionWrapper(
                date.today() - F('data_abertura'),
                output_field=models.IntegerField())
        )
        queryset = queryset.annotate(
            ate_vinte=Case(
                When(
                    Q(dias_abertura__gte=0) & Q(dias_abertura__lt=20),
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            ),
            vinte_trinta=Case(
                When(
                    Q(dias_abertura__gte=20) & Q(dias_abertura__lte=30),
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            ),
            trinta_mais=Case(
                When(
                    dias_abertura__gt=30,
                    then=Value(1)),
                default=Value(0), output_field=models.IntegerField()
            )
        )
        return queryset.aggregate(
            soma_ate_vinte=Sum('ate_vinte'),
            soma_vinte_trinta=Sum('vinte_trinta'),
            soma_trinta_mais=Sum('trinta_mais')
        )
