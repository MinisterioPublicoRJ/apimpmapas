from cached_property import cached_property
from django.conf import settings
from django.template import Context, Template

from dominio.alertas.dao import DetalheAlertaCompraDAO


class MensagemOuvidoriaCompras:
    alerta_sigla = "COMP"
    template_name = "dominio/alertas/templates/email_ouvidoria.html"

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = orgao_id
        self.alerta_id = alerta_id

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
        return Context(detalhe_alerta)

    def render(self):
        with open(self.template_name) as fobj:
            template = Template(fobj.read())

        return template.render(context=self.context)
