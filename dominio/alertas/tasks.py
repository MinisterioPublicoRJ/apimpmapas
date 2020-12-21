import celery
from celery.exceptions import MaxRetriesExceededError

from dominio.alertas.mail import envia_email_ouvidoria
from mprj_api.celeryconfig import app


class CustomTaskClass(celery.Task):

    def after_return(self, status, retval, task_id, args, kwargs, einfo=None):
        if status == "FAILURE":
            controller = args[0]
            controller.rollback()

    def on_success(self, retval, task_id, args, kwargs):
        controller = args[0]
        controller.success()


@app.task(base=CustomTaskClass, default_retry_delay=30, max_retries=3)
def async_envia_email_ouvidoria(controller):
    try:
        msg = controller.render_message()
        envia_email_ouvidoria(msg, controller.email_subject)
    except Exception as e:
        try:
            async_envia_email_ouvidoria.retry(exc=e)
        except MaxRetriesExceededError:
            pass
