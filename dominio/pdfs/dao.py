from django.conf import settings

from database.db_connect import Oracle_DB


class ItGateDAO:
    def get(self, it_gate_id):
        cursor = Oracle_DB.connect(
            settings.ORA_USER,
            settings.ORA_PASS,
            settings.ORA_HOST
        )
        query = '''
            SELECT itcn_arquivo
            FROM gate_info_tecnica
            WHERE itcn_dk = :it_id
        '''
        bindings = {'it_id': it_gate_id}
        result_set = Oracle_DB.execute(cursor, query, bindings=bindings)
        return (
            result_set
            if result_set
            else {"erro": "IT GATE não encontrada"}
        )
