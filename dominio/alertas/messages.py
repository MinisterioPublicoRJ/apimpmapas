from cached_property import cached_property
from django.template import Context, Template

from dominio.alertas.dao import DetalheAlertaCompraDAO


class MensagemOuvidoriaCompras:
    alerta_sigla = "COMP"
    template_name = "dominio/alertas/templates/email_ouvidoria.html"

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = orgao_id
        self.alerta_id = alerta_id

    @cached_property
    def context(self):
        detalhe_alerta = DetalheAlertaCompraDAO.get(alerta_id=self.alerta_id)
        return Context(detalhe_alerta)

    def render(self):
        with open(self.template_name) as fobj:
            template = Template(fobj.read())

        return template.render(context=self.context)
