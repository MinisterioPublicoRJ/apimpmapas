from django.conf import settings

from database.db_connect import Oracle_DB


class ItGateDAO:
    def serialize(self, result_set):
        return result_set

    def get(self, it_gate_id, request):
        cursor = Oracle_DB.connect(
            settings.DESAPARECIDOS_DB_USER,
            settings.DESAPARECIDOS_DB_PWD,
            settings.DESAPARECIDOS_DB_HOST
        )
        query = '''
            SELECT itcn_arquivo
            FROM gate_info_tecnica
            WHERE itcn_dk = :it_id
        '''
        bindings = {'it_id': it_gate_id}
        result_set = Oracle_DB.execute(cursor, query, bindings=bindings)
        return (
            self.serialize(result_set)
            if result_set
            else {"erro": "IT GATE não encontrada"}
        )
