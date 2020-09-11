from django.conf import settings

from dominio.alertas.tasks import async_envia_email_ouvidoria
from dominio.db_connectors import get_hbase_table


class BaseController:
    alerta_sigla = None
    hbase_cf = None
    hbase_table_name = None

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = str(orgao_id)
        self.alerta_id = str(alerta_id)

    @property
    def get_table(self):
        return get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_table_name
        )

    def get_row_key(self, orgao_id, alerta_id):
        return f"{orgao_id}_{self.alerta_sigla}_{alerta_id}".encode()

    def get_row_data(self, orgao_id, alerta_id):
        return {
            f"{self.hbase_cf}:orgao".encode(): orgao_id.encode(),
            f"{self.hbase_cf}:alerta_id".encode(): alerta_id.encode(),
            f"{self.hbase_cf}:sigla".encode(): self.alerta_sigla.encode(),
        }


class DispensaAlertaComprasController(BaseController):
    alerta_sigla = "COMP"
    hbase_cf = "dados_alertas"
    hbase_table_name = settings.HBASE_DISPENSAR_ALERTAS_TABLE

    def dispensa_para_orgao(self):
        row_key = self.get_row_key(self.orgao_id, self.alerta_id)
        data = self.get_row_data(self.orgao_id, self.alerta_id)
        self.get_table.put(row_key, data)

    def retorna_para_orgao(self):
        row_key = self.get_row_key(self.orgao_id, self.alerta_id)
        self.get_table.delete(row_key)

    def retorna_para_todos_orgaos(self):
        row_key = self.get_row_key("ALL", self.alerta_id)
        self.get_table.delete(row_key)

    def dispensa_para_todos_orgaos(self):
        row_key = self.get_row_key("ALL", self.alerta_id)
        data = self.get_row_data("ALL", self.alerta_id)
        self.get_table.put(row_key, data)


class EnviaAlertaComprasOuvidoriaController(BaseController):
    alerta_sigla = "COMP"
    hbase_cf = "dados_alertas"
    hbase_table_name = settings.HBASE_ALERTAS_OUVIDORIA_TABLE

    def rollback(self):
        row_key = self.get_row_key(self.orgao_id, self.alerta_id)
        self.get_table.delete(row_key)

    def success(self):
        dispensa_controller = DispensaAlertaComprasController(
            self.orgao_id,
            self.alerta_id
        )
        dispensa_controller.dispensa_para_todos_orgaos()

    @property
    def row_key(self):
        return self.get_row_key(self.orgao_id, self.alerta_id)

    @property
    def row_data(self):
        return self.get_row_data(self.orgao_id, self.alerta_id)

    @property
    def alerta_already_sent(self):
        result = self.get_table.scan(row_prefix=self.row_key)
        try:
            next(result)
            sent = True
        except StopIteration:
            sent = False

        return sent

    def save_alerta_state(self):
        self.get_table.put(
            self.row_key,
            self.row_data
        )

    def envia_email(self):
        async_envia_email_ouvidoria.delay(self)

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
