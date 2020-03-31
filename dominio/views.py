from datetime import datetime, timedelta

from django.conf import settings
from django.db import connections
from django.db.models import F
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView


from dominio import suamesa
from .db_connectors import run_query
from .mixins import CacheMixin, PaginatorMixin, JWTAuthMixin
from .models import Vista, Documento, Alerta, Usuario
from .serializers import (
    SaidasSerializer,
    OutliersSerializer,
    EntradasSerializer,
    DetalheAcervoSerializer,
    DetalheProcessosJuizoSerializer,
    SuaMesaListaVistasSerializer,
    AlertasListaSerializer,
)
from login.jwtlogin import authenticate_integra


@csrf_exempt
def login(request):
    response = authenticate_integra(request)
    usuario, created = Usuario.objects.get_or_create(
        username=response.get("username")
    )
    response["first_login"] = created
    response["first_login_today"] = created or usuario.get_first_login_today()
    usuario.save()

    return JsonResponse(response)


class DetalheAcervoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'DETALHE_ACERVO_CACHE_TIMEOUT'

    @staticmethod
    def get_variacao_orgao(l, orgao_id):
        for element in l:
            # orgao_id comes in position 0 of each element
            if element[0] == orgao_id:
                return element[4]
        return None

    @staticmethod
    def get_top_n_orgaos(l, n=3):
        sorted_list = sorted(l, key=lambda el: float(el[4]), reverse=True)
        result_list = [
            {
                'nm_promotoria': suamesa.format_text(el[1]),
                'variacao_acervo': el[4]
            }
            for el in sorted_list
        ]
        return result_list[:n]

    @staticmethod
    def get_acervo_increase(orgao_id, dt_inicio, dt_fim):
        query = """
                WITH tb_acervo_orgao_pct as (
                    SELECT *
                    FROM {namespace}.tb_acervo ac
                    INNER JOIN (
                        SELECT cod_pct
                        FROM {namespace}.atualizacao_pj_pacote
                        WHERE id_orgao = :orgao_id
                        ) org
                    ON org.cod_pct = ac.cod_atribuicao)
                SELECT
                    tb_data_fim.cod_orgao,
                    pc.orgi_nm_orgao as nm_orgao,
                    tb_data_fim.acervo_fim,
                    tb_data_inicio.acervo_inicio,
                    (acervo_fim - acervo_inicio)/acervo_inicio as variacao
                FROM (
                    SELECT cod_orgao, SUM(acervo) as acervo_fim
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_fim, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_fim
                INNER JOIN (
                    SELECT cod_orgao, SUM(acervo) as acervo_inicio
                    FROM tb_acervo_orgao_pct acpc
                    INNER JOIN {namespace}.tb_regra_negocio_investigacao regras
                        ON regras.cod_atribuicao = acpc.cod_atribuicao
                        AND regras.classe_documento = acpc.tipo_acervo
                    WHERE dt_inclusao = to_timestamp(:dt_inicio, 'yyyy-MM-dd')
                    GROUP BY cod_orgao
                    ) tb_data_inicio
                ON tb_data_fim.cod_orgao = tb_data_inicio.cod_orgao
                INNER JOIN {namespace}.atualizacao_pj_pacote pc
                ON pc.id_orgao = tb_data_fim.cod_orgao
                """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {
            'orgao_id': orgao_id,
            'dt_inicio': dt_inicio,
            'dt_fim': dt_fim
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        date_today = datetime.now().date()
        dt_fim = str(date_today)
        dt_inicio = date_today - timedelta(30)
        dt_inicio = '2020-02-10' if datetime(2020, 2, 10).date() > dt_inicio \
            else str(dt_inicio)
        n = 3

        data = self.get_acervo_increase(
            orgao_id=orgao_id,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )

        if not data:
            raise Http404

        variacao_acervo = self.get_variacao_orgao(data, orgao_id)
        top_n = self.get_top_n_orgaos(data, n=n)

        data_obj = {
            'variacao_acervo': variacao_acervo,
            'top_n': top_n
        }

        data = DetalheAcervoSerializer(data_obj).data
        return Response(data)


class OutliersView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'OUTLIERS_CACHE_TIMEOUT'
    _fields = [
        'cod_orgao',
        'acervo_qtd',
        'cod_atribuicao',
        'minimo',
        'maximo',
        'media',
        'primeiro_quartil',
        'mediana',
        'terceiro_quartil',
        'iqr',
        'lout',
        'hout',
        'dt_inclusao',
    ]

    def get_data(self, orgao_id):
        query = """
                SELECT
                cod_orgao,
                acervo,
                cod_atribuicao,
                minimo,
                maximo,
                media,
                primeiro_quartil,
                mediana,
                terceiro_quartil,
                iqr,
                lout,
                hout,
                dt_inclusao
                FROM {namespace}.tb_distribuicao
                WHERE cod_orgao = :orgao_id
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id
        }
        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_data(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404

        data_obj = dict(zip(self._fields, data[0]))

        data = OutliersSerializer(data_obj).data
        return Response(data)


class SaidasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SAIDAS_CACHE_TIMEOUT'

    def get_saidas(self, orgao_id):

        query = """
                SELECT saidas, id_orgao, cod_pct, percent_rank, dt_calculo
                FROM {namespace}.tb_saida
                WHERE id_orgao = :orgao_id
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_saidas(
            orgao_id=orgao_id
        )

        if not data:
            raise Http404

        fields = [
            'saidas',
            'id_orgao',
            'cod_pct',
            'percent_rank',
            'dt_calculo'
        ]
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data = SaidasSerializer(data_obj).data
        return Response(data)


class EntradasView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'ENTRADAS_CACHE_TIMEOUT'

    def get_entradas(self, orgao_id, nr_cpf):

        query = """
                SELECT
                    nr_entradas_hoje,
                    minimo,
                    maximo,
                    media,
                    primeiro_quartil,
                    mediana,
                    terceiro_quartil,
                    iqr,
                    lout,
                    hout
                FROM {namespace}.tb_dist_entradas
                WHERE comb_orga_dk = :orgao_id
                AND comb_cpf = :nr_cpf
                """.format(
                    namespace=settings.TABLE_NAMESPACE
                )
        parameters = {
            'orgao_id': orgao_id,
            'nr_cpf': nr_cpf
        }

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        nr_cpf = str(self.kwargs['nr_cpf'])

        data = self.get_entradas(
            orgao_id=orgao_id,
            nr_cpf=nr_cpf
        )

        if not data:
            raise Http404

        fields = [
            'nr_entradas_hoje',
            'minimo',
            'maximo',
            'media',
            'primeiro_quartil',
            'mediana',
            'terceiro_quartil',
            'iqr',
            'lout',
            'hout'
        ]
        data_obj = {
            fieldname: value for fieldname, value in zip(fields, data[0])
        }
        data = EntradasSerializer(data_obj).data
        return Response(data)


class SuaMesaVistasAbertas(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAVISTAS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        doc_count = Vista.vistas.abertas_promotor(orgao_id, cpf).count()

        return Response(data={"suamesa_vistas": doc_count})


class SuaMesaInvestigacoes(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAINVESTIGACOES_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_investigacoes = suamesa.get_regras(
            orgao_id,
            tipo='investigacao'
        )
        doc_count = Documento.investigacoes.em_curso(
            orgao_id, regras_investigacoes).count()

        return Response(data={"suamesa_investigacoes": doc_count})


class SuaMesaProcessos(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAPROCESSOS_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))

        regras_processos = suamesa.get_regras(orgao_id, tipo='processo')
        doc_count = Documento.processos.em_juizo(
            orgao_id, regras_processos).count()

        return Response(data={"suamesa_processos": doc_count})


class SuaMesaFinalizados(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESAFINALIZADOS_CACHE_TIMEOUT'
    fields = ["suamesa_finalizados"]

    def fetch_set(self, data):
        if not data:
            raise Http404

        return dict(zip(self.fields, data))

    def get_data(self, orgao_id):
        query = """
            select count(1)
            from {namespace}.mcpr_documento doc
            join {namespace}.mcpr_vista vista
                on doc.docu_dk = vista.vist_docu_dk
            join {namespace}.mcpr_andamento anda
                on vista.vist_dk = anda.pcao_vist_dk
            join ( select sub.stao_pcao_dk
                    from {namespace}.mcpr_sub_andamento sub
                    where sub.stao_tppr_dk in (6251,6657,6655,6644,6326,7912,
                                               6548,6326,6681,6678,6645,6682,
                                               6680,6679,6644,6668,6666,6665,
                                               6669,6667,6664,6655,6662,6659,
                                               6658,6663,6661,6660,6657,6670,
                                               6676,6674,6673,6677,6675,6672,
                                               6018,6341,6338,6019,6017,6591,
                                               6339,6553,7871,6343,6340,6342,
                                               6021,6334,6331,6022,6020,6593,
                                               6332,7872,6336,6333,6335,7745,
                                               6346,6345,6015,6016,6325,6327,
                                               6328,6329,6330,6337,6344,6656,
                                               6671,7869,7870,6324)
                ) sub
                on anda.pcao_dk = sub.stao_pcao_dk
            where year = year(date_sub(current_timestamp(),  30))
            and month >= month(date_sub(current_timestamp(),  30))
            and anda.pcao_dt_andamento >= date_sub(current_timestamp(),  30)
            and doc.docu_orgi_orga_dk_responsavel = :orgao_id
            group by doc.docu_orgi_orga_dk_responsavel
            order by doc.docu_orgi_orga_dk_responsavel;
        """.format(namespace=settings.TABLE_EXADATA_NAMESPACE)
        data = run_query(query, {"orgao_id": orgao_id})
        return self.fetch_set(data)

    def get(self, request, *args, **kwargs):
        orgao_id = kwargs.get("orgao_id")
        data = self.get_data(orgao_id)
        return Response(data=data)


class SuaMesaDetalheView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'SUAMESADETALHE_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")

        mesa_detalhe = Vista.vistas.agg_abertas_por_data(orgao_id, cpf)
        if all([v is None for v in mesa_detalhe.values()]):
            raise Http404

        return Response(mesa_detalhe)


class DetalheProcessosJuizoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'DETALHEPROCESSO_CACHE_TIMEOUT'

    @staticmethod
    def get_numero_acoes_propostas_pacote_atribuicao(orgao_id):
        query = """
            SELECT
                orgao_id,
                nm_orgao,
                nr_acoes_ultimos_60_dias,
                variacao_12_meses,
                nr_acoes_ultimos_30_dias
            FROM {namespace}.tb_detalhe_processo t1
            JOIN (
                SELECT cod_pct
                FROM {namespace}.tb_detalhe_processo
                WHERE orgao_id = :orgao_id) t2
              ON t1.cod_pct = t2.cod_pct
        """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {
            'orgao_id': orgao_id
        }
        return run_query(query, parameters)

    @staticmethod
    def get_value_from_orgao(l, orgao_id, value_position=2):
        for element in l:
            # orgao_id comes in position 0 of each element
            if element[0] == orgao_id:
                return element[value_position]
        return None

    @staticmethod
    def get_top_n_orgaos(l, n=3):
        sorted_list = sorted(l, key=lambda el: el[4], reverse=True)
        result_list = [
            {
                'nm_promotoria': suamesa.format_text(el[1]),
                'nr_acoes_propostas_30_dias': el[4]
            }
            for el in sorted_list
        ]
        return result_list[:n]

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data_acoes = self.get_numero_acoes_propostas_pacote_atribuicao(
            orgao_id=orgao_id
        )

        if not data_acoes:
            raise Http404

        nr_acoes_60_dias = self.get_value_from_orgao(
            data_acoes, orgao_id, value_position=2)
        variacao_acoes_12_meses = self.get_value_from_orgao(
            data_acoes, orgao_id, value_position=3)
        top_n = self.get_top_n_orgaos(data_acoes, n=3)

        data_obj = {
            'nr_acoes_propostas_60_dias': nr_acoes_60_dias,
            'variacao_12_meses': variacao_acoes_12_meses,
            'top_n': top_n
        }

        data = DetalheProcessosJuizoSerializer(data_obj).data
        return Response(data)


class SuaMesaVistasListaView(
        JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'SUAMESAVISTASLISTA_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = kwargs.get("cpf")
        abertura = kwargs.get("abertura")
        lista_aberturas = ("ate_vinte", "vinte_trinta", "trinta_mais")
        page = int(request.GET.get("page", 1))

        if abertura not in lista_aberturas:
            msg = "data_abertura inválida. "\
                  f"Opções são: {', '.join(lista_aberturas)}"
            return Response(data=msg, status=404)

        data = Vista.vistas.abertas_por_data(orgao_id, cpf).filter(
            **{abertura: 1}
        ).order_by('-data_abertura').values(
            numero_mprj=F("documento__docu_nr_mp"),
            numero_externo=F("documento__docu_nr_externo"),
            dt_abertura=F("data_abertura"),
            classe=F("documento__classe__descricao")
        )
        page_data = self.paginate(
            data,
            page=page,
            page_size=suamesa.VISTAS_PAGE_SIZE
        )

        vistas_lista = SuaMesaListaVistasSerializer(page_data, many=True).data

        return Response(data=vistas_lista)


class AlertasView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'ALERTAS_CACHE_TIMEOUT'
    # TODO: Mover constante para um lugar decente
    ALERTAS_SIZE = 25

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        page = int(request.GET.get("page", 1))

        data = Alerta.validos_por_orgao(orgao_id)
        page_data = self.paginate(
            data,
            page=page,
            page_size=self.ALERTAS_SIZE
        )

        alertas_lista = AlertasListaSerializer(page_data, many=True)

        return Response(data=alertas_lista.data)


class TempoTramitacaoView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = 'TEMPO_TRAMITACAO_CACHE_TIMEOUT'
    fields = [
        "id_orgao",
        "media_orgao",
        "minimo_orgao",
        "maximo_orgao",
        "mediana_orgao",
        "media_pacote",
        "minimo_pacote",
        "maximo_pacote",
        "mediana_pacote",
        "media_pacote_t1",
        "minimo_pacote_t1",
        "maximo_pacote_t1",
        "mediana_pacote_t1",
        "media_orgao_t1",
        "minimo_orgao_t1",
        "maximo_orgao_t1",
        "mediana_orgao_t1",
        "media_pacote_t2",
        "minimo_pacote_t2",
        "maximo_pacote_t2",
        "mediana_pacote_t2",
        "media_orgao_t2",
        "minimo_orgao_t2",
        "maximo_orgao_t2",
        "mediana_orgao_t2",
    ]

    def get_data(self, orgao_id):
        query = """
            SELECT * FROM {namespace}.tb_tempo_tramitacao
            WHERE id_orgao = :orgao_id
        """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {"orgao_id": orgao_id}

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])

        data = self.get_data(orgao_id)

        if not data:
            raise Http404

        ser_data = dict(zip(self.fields, data[0]))
        return Response(ser_data)


class DesarquivamentosView(JWTAuthMixin, CacheMixin, APIView):
    cache_config = "DESARQUIVAMENTOS_CACHE_TIMEOUT"
    fields = ["numero_mprj", "qtd_desarq"]

    def fetch_set(self, cursor):
        return [dict(zip(self.fields, row)) for row in cursor.fetchall()]

    def get_data(self, orgao_id):
        with connections["dominio_db"].cursor() as cursor:
            query = """
                WITH AGRUPADOS AS (SELECT d.docu_nr_mp, COUNT(d.docu_nr_mp)
                FROM MCPR_DOCUMENTO d
                JOIN mcpr_vista v ON v.vist_docu_dk = d.docu_dk
                JOIN mcpr_andamento a ON a.pcao_vist_dk = v.vist_dk
                JOIN mcpr_sub_andamento sa ON sa.stao_pcao_dk = a.pcao_dk
                JOIN mcpr_tp_andamento ta ON ta.tppr_dk = sa.stao_tppr_dk
                WHERE sa.stao_tppr_dk IN (6075, 1028, 6798, 7245, 6307, 1027,
                                          7803, 6003, 7802, 7801)
                                          AND d.docu_cldc_dk = 392
                AND d.DOCU_ORGI_ORGA_DK_RESPONSAVEL = %s
                GROUP BY docu_nr_mp, a.pcao_dt_andamento)
                SELECT docu_nr_mp, COUNT(docu_nr_mp)
                FROM AGRUPADOS GROUP BY docu_nr_mp
            """
            result_set = cursor.execute(query, [orgao_id])
            return self.fetch_set(result_set)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        # TODO: pensar numa forma geral de discernir 404 de respostas
        # vazias e respostas não existentes

        return Response(data=self.get_data(orgao_id))


class ListaProcessosView(JWTAuthMixin, CacheMixin, PaginatorMixin, APIView):
    cache_config = 'LISTA_PROCESSOS_CACHE_TIMEOUT'
    PROCESSOS_SIZE = 20

    def get_data(self, orgao_id):
        query = """
            SELECT * FROM {namespace}.tb_lista_processos
            WHERE orgao_dk = :orgao_id
            ORDER BY dt_ultimo_andamento DESC
        """.format(namespace=settings.TABLE_NAMESPACE)
        parameters = {"orgao_id": orgao_id}

        return run_query(query, parameters)

    def get(self, request, *args, **kwargs):
        orgao_id = int(self.kwargs['orgao_id'])
        page = int(request.GET.get("page", 1))

        data = self.get_data(orgao_id)

        if not data:
            raise Http404

        fields = [
            'id_orgao',
            'classe_documento',
            'docu_nr_mp',
            'docu_nr_externo',
            'docu_etiqueta',
            'docu_personagens',
            'dt_ultimo_andamento',
            'ultimo_andamento',
            'url_tjrj'
        ]
        data_obj = [dict(zip(fields, row)) for row in data]

        page_data = self.paginate(
            data_obj,
            page=page,
            page_size=self.PROCESSOS_SIZE
        )

        return Response(data=page_data)
