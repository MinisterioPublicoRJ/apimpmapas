from django.conf import settings

from dominio.alertas.tasks import async_envia_email_ouvidoria
from dominio.db_connectors import get_hbase_table


class EnviaAlertaComprasOuvidoriaController:
    alerta_sigla = "COMP"
    hbase_cf = "dados_alertas"

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = str(orgao_id)
        self.alerta_id = str(alerta_id)

    @classmethod
    def get_table(cls):
        return get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_ALERTAS_OUVIDORIA_TABLE
        )

    @classmethod
    def rollback_envio(cls, orgao_id, alerta_sigla, alerta_id):
        row_key = cls.get_row_key(orgao_id, alerta_sigla, alerta_id)
        cls.get_table().delete(row_key)

    @classmethod
    def get_row_key(cls, orgao_id, alerta_sigla, alerta_id):
        return (
            f"alerta_ouvidoria_{orgao_id}_{alerta_sigla}_{alerta_id}"
        ).encode()

    @property
    def row_key(self):
        return self.get_row_key(
            self.orgao_id,
            self.alerta_sigla,
            self.alerta_id
        )

    @property
    def row_data(self):
        return {
            f"{self.hbase_cf}:orgao".encode(): self.orgao_id.encode(),
            f"{self.hbase_cf}:alerta_id".encode(): self.alerta_id.encode(),
            f"{self.hbase_cf}:sigla".encode(): self.alerta_sigla.encode(),
        }

    @property
    def alerta_already_sent(self):
        result = self.get_table().scan(row_prefix=self.row_key)
        try:
            next(result)
            sent = True
        except StopIteration:
            sent = False

        return sent

    def save_alerta_state(self):
        self.get_table().put(
            self.row_key,
            self.row_data
        )

    def envia_email(self):
        async_envia_email_ouvidoria.delay(
            self.orgao_id,
            self.alerta_sigla,
            self.alerta_id,
        )

    def prepara_resposta(self, already_sent):
        # TODO: talvez levantar excessão e tratar na view
        status = 201
        msg = "Alerta enviado para ouvidoria com sucesso"

        if already_sent:
            status = 409
            msg = "Este alerta já foi enviado para ouvidoria"

        resp = {"detail": msg}

        return resp, status

    def envia(self):
        already_sent = self.alerta_already_sent
        if not already_sent:
            self.save_alerta_state()
            self.envia_email()

        return self.prepara_resposta(already_sent)
