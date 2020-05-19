from rest_framework.response import Response
from rest_framework.views import APIView

from dominio.tutela import suamesa
from dominio.mixins import CacheMixin, JWTAuthMixin
from dominio.models import Vista, Documento, SubAndamento
from dominio.pip.utils import get_orgaos_same_aisps

#JWTAuthMixin
class SuaMesaView(CacheMixin, APIView):
    cache_config = 'SUAMESA_CACHE_TIMEOUT'

    def get(self, request, *args, **kwargs):
        orgao_id = int(kwargs.get("orgao_id"))
        cpf = request.GET.get("cpf", None)
        tipo = request.GET.get("tipo", None)

        if not tipo:
            # Definir erro
            return Response(data={"erro": "Sem tipo"})

        if tipo == 'vistas':
            doc_count = Vista.vistas.abertas_promotor(orgao_id, cpf).count()
        elif tipo == 'tutela_investigacoes':
            regras = [51219, 51220, 51221, 51222, 51223, 392, 395]
            doc_count = Documento.investigacoes.em_curso(
                orgao_id, regras).count()
        elif tipo == 'tutela_processos':
            regras = [18, 126, 51218, 323, 319, 320, 441, 127, 582, 159, 175, 176, 177, 51205, 51217]
            doc_count = Documento.processos.em_juizo(
                orgao_id, regras).count()
        elif tipo == 'finalizados':
            regras_saidas = (6251, 6657, 6655, 6644, 6326)
            regras_arquiv = (7912, 6548, 6326, 6681, 6678, 6645, 6682, 6680, 6679,
                            6644, 6668, 6666, 6665, 6669, 6667, 6664, 6655, 6662,
                            6659, 6658, 6663, 6661, 6660, 6657, 6670, 6676, 6674,
                            6673, 6677, 6675, 6672, 6018, 6341, 6338, 6019, 6017,
                            6591, 6339, 6553, 7871, 6343, 6340, 6342, 6021, 6334,
                            6331, 6022, 6020, 6593, 6332, 7872, 6336, 6333, 6335,
                            7745, 6346, 6345, 6015, 6016, 6325, 6327, 6328, 6329,
                            6330, 6337, 6344, 6656, 6671, 7869, 7870, 6324)

            regras = regras_saidas + regras_arquiv
            doc_count = SubAndamento.finalizados.trinta_dias(
                orgao_id, regras)\
                .values('andamento__vista__documento__docu_dk')\
                .distinct()\
                .count()
        elif tipo == 'pip_inqueritos':
            doc_count = Documento.investigacoes.em_curso(
                orgao_id, [3, 494]
            ).count()
        elif tipo == 'pip_pics':
            doc_count = Documento.investigacoes.em_curso(
                orgao_id, [590]
            ).count()
        elif tipo == 'pip_aisp':
            _, orgaos_same_aisp = get_orgaos_same_aisps(orgao_id)

            doc_count = Documento.investigacoes.em_curso_grupo(
                orgaos_same_aisp, [3, 494, 590]
            ).count()
        else:
            # Definir erro
            return Response(data={"erro": "Tipo desconhecido"})

        return Response(data={"nr_documentos": doc_count})
