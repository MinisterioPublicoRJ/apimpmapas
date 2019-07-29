from unittest import mock

from decouple import config
from django.test import TestCase
from django.utils import timezone
from model_mommy.mommy import make

from api.serializers import DadoSerializer
from api.exceptions import QueryError


class MailTest(TestCase):

    @mock.patch('api.serializers.dado_template')
    @mock.patch('api.serializers.send_mail')
    @mock.patch('api.serializers.login', return_value='login')
    @mock.patch('api.serializers.execute')
    def test_email_send(self, _execute, _login, _send_mail, _dado_template):
        except_message = 'test_error'
        _dado_template.render.return_value = 'Mensagem de teste'
        _execute.side_effect = QueryError(except_message)

        entidade = make('api.Entidade')
        dado = make('api.Dado', title='dado de teste', entity_type=entidade)
        DadoSerializer(dado, domain_id='00').data

        _send_mail.assert_called_once_with(
            server='login',
            msg='Mensagem de teste',
            dest=config('MAIL_DESTINATION'),
            subject="Erro no dado {}".format(dado.title)
        )

        _dado_template.render.assert_called_once_with(
            dado_titulo=dado.title,
            dado_entidade=dado.entity_type.name,
            msg=except_message,
            datetime=timezone.localtime().strftime("%d/%m/%Y %H:%M:%S ")
        )
