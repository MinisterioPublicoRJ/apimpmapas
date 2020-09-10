import celery
from celery.exceptions import MaxRetriesExceededError

from dominio.alertas.mail import envia_email_ouvidoria
from mprj_api.celeryconfig import app


class CustomTaskClass(celery.task.Task):

    def after_return(self, status, retval, task_id, args, kwargs, einfo=None):
        if status == "FAILURE":
            from dominio.alertas.controllers import (
                EnviaAlertaComprasOuvidoriaController
            )

            orgao_id, alerta_id = args[0], args[-1]
            EnviaAlertaComprasOuvidoriaController.rollback_envio(
                orgao_id,
                alerta_id
            )

    def on_success(self, retval, task_id, args, kwargs):
        from dominio.alertas.controllers import DispensaAlertaComprasController

        alerta_id = args[-1]
        DispensaAlertaComprasController.dispensa_para_todos_orgaos(alerta_id)


@app.task(base=CustomTaskClass, default_retry_delay=30, max_retries=3)
def async_envia_email_ouvidoria(orgao_id, alerta_sigla, alerta_id):
    try:
        msg = "message"
        envia_email_ouvidoria(msg)
    except Exception as e:
        try:
            async_envia_email_ouvidoria.retry(exc=e)
        except MaxRetriesExceededError:
            pass
