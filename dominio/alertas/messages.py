from cached_property import cached_property
from django.conf import settings
from django.template import Context, Template

from dominio.alertas.dao import DetalheAlertaCompraDAO


class MensagemOuvidoria:
    alerta_sigla = None
    template_name = None

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = orgao_id
        self.alerta_id = alerta_id

    @property
    def context(self):
        raise NotImplementedError()

    def render(self):
        with open(self.template_name) as fobj:
            template = Template(fobj.read())

        return template.render(context=Context(self.context))


class MensagemOuvidoriaCompras(MensagemOuvidoria):
    alerta_sigla = "COMP"
    template_name = "dominio/alertas/templates/email_ouvidoria_compras.html"

    def get_link_painel(self, contratacao):
        return settings.URL_PAINEL_COMPRAS\
            .replace("{contrato_iditem}", self.alerta_id)\
            .replace("{contratacao}", str(contratacao))

    @cached_property
    def context(self):
        detalhe_alerta = DetalheAlertaCompraDAO.get(alerta_id=self.alerta_id)
        detalhe_alerta["link_painel"] = self.get_link_painel(
            detalhe_alerta["contratacao"]
        )
        return detalhe_alerta


class MensagemOuvidoriaISPS(MensagemOuvidoria):
    alerta_sigla = "ISPS"
    template_name = "dominio/alertas/templates/email_ouvidoria_isps.html"
