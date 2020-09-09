from django.conf import settings

from dominio.db_connectors import get_hbase_table


class EnviaAlertaComprasOuvidoriaController:
    alerta_sigla = "COMP"

    def __init__(self, orgao_id, alerta_id):
        self.orgao_id = orgao_id
        self.alerta_id = alerta_id

    @property
    def get_row_key(self):
        return (
            f"alerta_ouvidoria_{self.orgao_id}_{self.alerta_sigla}_"
            f"{self.alerta_id}"
        )

    @property
    def get_table(self):
        return get_hbase_table(
            settings.PROMOTRON_HBASE_NAMESPACE
            +
            settings.HBASE_ALERTAS_OUVIDORIA_TABLE
        )

    @property
    def alerta_already_sent(self):
        result = self.get_table.scan(row_prefix=self.get_row_key)
        try:
            next(result)
            sent = True
        except StopIteration:
            sent = False

        return sent

    @property
    def get_row_data(self):
        return True

    def save_alerta_state(self):
        self.get_table.put(
            self.get_row_key.encode(),
            self.get_row_data
        )

    def envia(self):
        already_sent = self.alerta_already_sent
        if not already_sent:
            self.save_alerta_state()
