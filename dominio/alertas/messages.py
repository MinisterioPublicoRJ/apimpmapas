from django.template import Context, Template


class MensagemOuvidoriaCompras:
    alerta_sigla = "COMP"
    template_name = "dominio/alertas/templates/email_ouvidoria.html"

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = orgao_id
        self.alerta_id = alerta_id

    @property
    def context(self):
        return Context(
            {"orgao_id": self.orgao_id, "alerta_id": self.alerta_id}
        )

    def render(self):
        with open(self.template_name) as fobj:
            template = Template(fobj.read())

        return template.render(context=self.context)
