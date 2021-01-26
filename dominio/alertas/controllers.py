from django.conf import settings

from dominio.alertas import messages
from dominio.alertas.tasks import async_envia_email_ouvidoria
from dominio.db_connectors import get_hbase_table


class HBaseAccessController:
    hbase_cf = None
    hbase_table_name = None
    hbase_all_cf = None
    hbase_all_table_name = None

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

    @property
    def get_all_table(self):
        return get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            self.hbase_all_table_name
        )

    def get_row_key(self, alerta_id):
        return f"{alerta_id}".encode()

    def get_row_data(self, orgao_id, alerta_id):
        sigla = alerta_id.split('.')[0]
        return {
            f"{self.hbase_cf}:orgao".encode(): orgao_id.encode(),
            f"{self.hbase_cf}:alerta_id".encode(): alerta_id.encode(),
            f"{self.hbase_cf}:sigla".encode(): sigla.encode(),
        }


class DispensaAlertaController(HBaseAccessController):
    def dispensa_para_orgao(self):
        row_key = self.get_row_key(self.alerta_id)
        data = self.get_row_data(self.orgao_id, self.alerta_id)
        self.get_table.put(row_key, data)

    def retorna_para_orgao(self):
        row_key = self.get_row_key(self.alerta_id)
        self.get_table.delete(row_key)

    def retorna_para_todos_orgaos(self):
        row_key = self.get_row_key(".".join(self.alerta_id.split(".")[:-1]))
        self.get_all_table.delete(row_key)

    def dispensa_para_todos_orgaos(self):
        alrt_key = ".".join(self.alerta_id.split(".")[:-1])
        row_key = self.get_row_key(alrt_key)
        data = self.get_row_data("ALL", alrt_key)
        self.get_all_table.put(row_key, data)


class DispensaAlertaController(DispensaAlertaController):
    hbase_cf = "dados_alertas"
    hbase_table_name = settings.HBASE_DISPENSAR_ALERTAS_TABLE
    hbase_all_cf = "dados_alertas"
    hbase_all_table_name = settings.HBASE_DISPENSAR_ALLALERTAS_TABLE


class EnviaAlertaOuvidoriaController(HBaseAccessController):
    dispensa_controller_class = None
    messager_class = None

    def rollback(self):
        self.get_table.delete(self.row_key)

    def success(self):
        dispensa_controller = self.dispensa_controller_class(
            self.orgao_id,
            self.alerta_id
        )
        dispensa_controller.dispensa_para_todos_orgaos()

    @property
    def row_key(self):
        return self.get_row_key(self.alerta_id)

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

    def render_message(self):
        messager = self.messager_class(self.orgao_id, self.alerta_id)
        return messager.render()

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


class EnviaAlertaComprasOuvidoriaController(EnviaAlertaOuvidoriaController):
    alerta_sigla = "COMP"
    hbase_cf = "dados_alertas"
    hbase_table_name = settings.HBASE_ALERTAS_OUVIDORIA_TABLE

    email_subject = settings.EMAIL_SUBJECT_OUVIDORIA_COMPRAS

    dispensa_controller_class = DispensaAlertaController
    messager_class = messages.MensagemOuvidoriaCompras


class EnviaAlertaISPSOuvidoriaController(EnviaAlertaOuvidoriaController):
    alerta_sigla = "ISPS"
    hbase_cf = "dados_alertas"
    hbase_table_name = settings.HBASE_ALERTAS_OUVIDORIA_TABLE

    email_subject = settings.EMAIL_SUBJECT_OUVIDORIA_SANEAMENTO

    dispensa_controller_class = DispensaAlertaController
    messager_class = messages.MensagemOuvidoriaISPS
